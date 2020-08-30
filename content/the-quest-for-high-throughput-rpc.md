Date: 2018-07-07 12:30 am
Tags: misc
Authors: Sharath Gururaj
Title: The quest for high throughput RPC
disqus_identifier: the-quest-for-high-throughput-rpc


In this post, I compare the rpc throughput of some existing RPC frameworks and talk about a new technique of doing RPC . Dropwizard on a single connection gives around `1000 req/sec`, whereas a prototype implementation of this technique gives around `4 million req/sec` for a “hello world” rpc

Lots of companies these days use a microservices architecture, where the application as a whole is split into multiple smaller microservices communicating over the network. What follows in the post is heavy on numbers, which admittedly is boring to parse and makes it a little dry. A nanosec, microsec and a millisec might all just seem like a really small amount of time for humans but the distance between them is vast. If we were to blow up the numbers to human scale and make a nanosec as a second, then it would take one nanosec to pick up a pen next to your laptop, one microsec is a 20 min bike ride, and 1 millisec is a bike ride from bangalore to indore!

For the time being, I’m going to consider two communicating processes on localhost so we don’t have to worry about network transmission latency for now
Our goal is to exchange 100 byte messages as fast as we can between two processes with a cap on (say 95% percentile) latency (say, `<5 ms`)

## Dropwizard and web services
If we hook up a simple dropwizard app with a “hello world” GET api and hit it with apache bench (ab) on localhost laptop with a single connection, I get around `1000 req/sec`

If I pump up the number of concurrent connections, I get around `7000 req/s` with around 100 connections (I hit ulimit after that on mac).

How good or bad is that?

For an absolute theoretical limit, we can compare it to the rate at which CPUs can read and write streaming data to/from memory. From my measurements, each core can stream data from RAM at around 1GB/sec.
so 1GBps means 10 million req/s with 100 byte messages. When compared to the 800 req/s for a single connection, this is disappointing indeed.

Of course, dropwizard does a lot more than simply stream data to/from memory. It has to parse http, send the packet down on the tcp stack and do the whole thing back on the rx side.

So how much time does it take for a packet to traverse the tcp stack? I’ve measured that it takes around ~25 microseconds ballpark to go down or come up the tcp stack. This is also in agreement with some online benchmarks. If we take this into account, it should take around 1/(50 usec) or ~2000 req/sec per core (pair). Compared to this, 800 req/s seems to be a bit too slow, even with the added http parsing.

With multiple cores and a large number of connections, I was able to crank up dropwizard to around 20K req/sec, but it requires many 100’s of connections to parallelize the processing. But keeping in mind the 10 million req/sec, this is still disappointing

The problem with using jetty/dropwizard for RPC is that, fundamentally, the architectures these web servers are tuned for entirely different things. Web servers are meant to operate on the internet, where a server can hold many tens of thousands of browser connections, with each browser connection being mostly idle and bursty for a short while. This does not map well to a Data Center environment where a server is talking to only about a dozen other services, and the connections are long lived and required to be very high throughput.

I believe this is causing a systemic performance problem in software companies. For example, we are all aware that disk and database access is orders of magnitude slower than cpu/network. Why then do we put ~20 dropwizard boxes in front of a mysql DB? Shouldn’t it be the other way round? 1 (or a few for redundancy) dropwizard box fronting multiple sharded mysql instances? This webserver problem leads to a vicious cycle: Each client needs to also employ multiple boxes just to generate the paralellism and connections to load a server.

The summary so far:

| type      | throughput |
| ----------- | ----------- |
| dropwizard single connection      | 1000 req/s       |
| dropwizard 100 connections   | 7000 req/s        |
| TCP packet round trip   | 20k req/s (ballpark)        |
| CPU streaming from RAM   | 10M req/s        |



## Unix domain sockets

Anyway, to continue with our quest for high throughput, lets skip web servers altogether.

With Unix domain sockets (which works only on localhost), we can bypass the entire tcp stack and take a much shorter route through the kernel. With UDS and a netty server (the default implementation in specter), we have measured around 10K req/s on a single core. Compare this to 800 req/s for dropwizard and 20K req/s if we were to traverse the TCP stack). With all cores (~10 cores), I measured around 40K req/s. This is much better than web servers. But still slow, considering
* we’re skipping the entire tcp stack
* the 1GBps CPU-memory bandwidth


| type      | throughput |
| ----------- | ----------- |
| UDS single connection      | 10K req/s       |
| UDS multiple connections   | 40K req/s        |




## Grpc and HTTP2

Another fundamental problem with all the previous frameworks are that they operate in inherently thread-request-response modes. i.e., the client thread sends a request and waits for a response. We would be able to achieve much better results if we operate in streaming mode, where the client is streaming multiple requests and the server is streaming back multiple responses. For this, we use HTTP2. It has two big advantages, the wire format is binary (not textual like HTTP) and it supports request streaming/pipelining

gRPC is a RPC mechanism using HTTP2. I haven’t explicitly measured the performance but according to the available online bencharks, they are able to do around 300K req/sec across two different machines, (which I assume will fall to ~150K) with both client and server on localhost.

Newer versions of jetty also support HTTP2. I tested out with a barebones embedded HTTP2 jetty server and I was able to get ~40K req/sec which is comparable to the UDS performance. Although less than gRPC, This is impressive considering that jetty has to parse HTTP as well as traverse the tcp stack, which UDS avoids. (Also remember that UDS is operating in request-response mode, not streaming mode)

## Raw sockets

All this begs the question: what is the fundamental limit for streaming data across a TCP connection? I threw up a small experiment with raw sockets in java on localhost and to my surprise, I was able to get the full 1GBps even with the tcp stack. Then where are we going wrong? why aren’t we able to achieve this with existing frameworks and even with http2?
When I was running the TCP streaming test, I realized that the key to high throughput is batching. The cost of traversing the tcp stack is roughly the same whether we send 1 byte or 1kB or 1MB. This is very apparent in the tests. With small messages, the throughput is approx 10K req/s. As we double the message size, the throughput keeps doubling, until it reaches 1GBps. So it makes sense to introduce a small “linger” time to combine multiple messages and send it across at once. How big is “big” for TCP networks? From the tests, I found that ~ 10Kb payload size is able to saturate the network (and memory) line rates

None of the RPC frameworks that I know of employ this technique. Actually, Kafka producer employs batching but suffers from other architectural issues which prevents it from achieving full line rate (More on that in a future post). In fact, the trend is in the opposite direction, to reduce message latencies further and send across a message as soon as possible. For example, Aeron claims to reduce latency from 50 microsec to 30 microsec by using UDP. The latency improvement might be super important in finance but presents only a very marginal improvements in throughput.

## The new and shiny
I wrote a client and a server which uses this batching technique over raw sockets. I batch small messages together until they reach a size of 20KB (or a timeout expires) and send big batches (~20kb) over tcp. The results were quite astounding. I was able to reach 3 million req/sec with 100 byte messages and only a single tcp connection and a single core (pair).

| type      | throughput |
| ----------- | ----------- |
| gRPC      | 150K req/s (haven't tested)      |
| Jetty HTTP2 server with async client and req pipelining    | 40K req/s        |
| Aeron    | 30K req/s        |


The code has almost no micro-optimizations (like object cache, zero copy, connection pools, etc) but it demostrates the effectiveness of this architecture.I am a little blown away by how much the throughput increasing with a simple technique. The best news is that the throughput remains virtually unaffected even over a 10Gbps network
If you’re interested in checking out the code and trying it out on localhost or in our DC, here is the link.
https://github.com/agsha/sharpc

| type      | throughput |
| ----------- | ----------- |
| <span style="color:red">New Batching RPC single TCP connection</span> | 3M req/s (haven't tested)      |


## Summary

* Dropwizard/jetty has a well understood and rock solid programming model, but leaves a lot to be desired with respect to max throughput achievable.
* Enabling HTTP2 is quite trivial for Jetty and can be expected to fetch ~30–50% increase in throughput
* Maybe its time to consider a “true” RPC subsystem in software companies: like grpc or thrift
* A batching algorithm can increase throughput by orders of magnitude compared to even high performance frameworks like grpc
and here’s a cat of all the previous tables

| type      | throughput |
| ----------- | ----------- |
| dropwizard single connection      | 1000 req/s       |
| dropwizard 100 connections   | 7000 req/s        |
| TCP packet round trip   | 20k req/s (ballpark)        |
| CPU streaming from RAM   | 10M req/s        |
| UDS single connection      | 10K req/s       |
| UDS multiple connections   | 40K req/s        |
| gRPC      | 150K req/s (haven't tested)      |
| Jetty HTTP2 server with async client and req pipelining    | 40K req/s        |
| Aeron    | 30K req/s        |
| <span style="color:red">New Batching RPC single TCP connection</span>  | 3M req/s (haven't tested)      |




