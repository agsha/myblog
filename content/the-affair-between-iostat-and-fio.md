Date: 2016-06-02 04:20 pm
Tags: misc
Authors: Sharath Gururaj
Title: The affair between iostat and fio 
disqus_identifier: c_ide


In the following analysis, I'm going to assume you already know what `fio` and `iostat` is (I'm too lazy to write it down, and there are better articles out there). This post merely explains the relationship between the numbers

### fio output

```
[sharath.g@prod-d42ar-osd-a-00079-423040 /mnt/vdb1]$ sudo fio --name=global --bs=4k --ioengine=libaio --iodepth=1 --runtime=120 --time_based --size=3G --group_reporting --disable_lat=1 --disable_clat=1 --disable_slat=1 --clat_percentiles=0  --filename=/mnt/vdb1/fio/myfile --name=regular_read --rw=randread
regular_read: (g=0): rw=randread, bs=4K-4K/4K-4K, ioengine=libaio, iodepth=1
2.0.8
Starting 1 process
regular_read: Laying out IO file(s) (1 file(s) / 3072MB)
Jobs: 1 (f=1): [r] [24.0% done] [672K/0K /s] [168 /0  iops] [eta 01m:32s]

```

[sharath.g@prod-d42ar-osd-a-00079-423040 /home/sharath.g]$ sudo fio --name=global --bs=4k --ioengine=libaio --iodepth=1 --runtime=30 --time_based --size=3G --group_reporting --disable_lat=1 --disable_clat=1 --disable_slat=1 --clat_percentiles=0  --filename=/mnt/vdb1/fio/myfile --name=regular_read --rw=randread
regular_read: (g=0): rw=randread, bs=4K-4K/4K-4K, ioengine=libaio, iodepth=1
2.0.8
Starting 1 process
Jobs: 1 (f=1): [r] [100.0% done] [708K/0K /s] [177 /0  iops] [eta 00m:00s]
regular_read: (groupid=0, jobs=1): err= 0: pid=28099
  read : io=21060KB, bw=718776 B/s, iops=175 , runt= 30003msec
    bw (KB/s)  : min=  640, max=  798, per=100.00%, avg=702.34, stdev=36.92
  cpu          : usr=0.09%, sys=0.44%, ctx=5274, majf=0, minf=20
  IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued    : total=r=5265/w=0/d=0, short=r=0/w=0/d=0

Run status group 0 (all jobs):
   READ: io=21060KB, aggrb=701KB/s, minb=701KB/s, maxb=701KB/s, mint=30003msec, maxt=30003msec

Disk stats (read/write):
  vdb: ios=5251/0, merge=0/0, ticks=29828/0, in_queue=29820, util=99.40%


analysis:
  read : io=21060KB, bw=718776 B/s, iops=175 , runt= 30003msec
issued    : total=r=5265/w=0/d=0, short=r=0/w=0/d=0
Disk stats (read/write):
  vdb: ios=5251/0, merge=0/0, ticks=29828/0, in_queue=29820, util=99.40%

io = bw*runt
io = iops*runt*bs
issued(r) = iops*runt
io = ios*bs

### iostat output

````
[sharath.g@prod-d42ar-osd-a-00079-423040 /home/sharath.g]$ iostat -x -d 2 /dev/vdb 
Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
vdb               0.00     0.00  179.00    0.00   716.00     0.00     8.00     1.00    5.59    5.59    0.00   5.58  99.80
### some inferences
From the line `read : io=78556KB, bw=670322 B/s, iops=163 , runt=120004msec` 
we observe that `io = bw * runt`. Makes sense.

```
### iostat output

````
[sharath.g@prod-d42ar-osd-a-00050-409388 /home/sharath.g]$ iostat -x  -d 2 /dev/vdb
Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
vdb               0.00     0.00  165.00    0.00   660.00     0.00     8.00     0.99    6.02    6.02    0.00   6.02  99.40
````
### units
`bs = bytes`, `io = KB` `bw=KBps`, `runt = ms` `r/s=number` `avrq-sz=sectors (=512 bytes)`

### some inferences
From the line `read : io=78556KB, bw=670322 B/s, iops=163 , runt=120004msec` 
we observe that `io = bw * runt`. Makes sense.


### libaio,read,sync=0,direct=0
* `bw = bs*iops`
* `io = bs*iops*(runt/1000) / 1024`
* `rKB/s = r/s * (avgrq-sz*512) / 1024`

Observe the `r/s`, `rKB/s` and `avrq-sz` graphs. Its very interesting. until block size of 4kb, the `iops` value remains constant at 175. After this size, the `avrq-sz` starts doubling (the file system minimum block size is 4kb but it can increase that block size upto 0.5 mb when we are trying to read bigger blocks). So after bs=4kb, iops drops because there is some time required to do sequential reads as well. It hits a low at 512kb because reading 512kb is eating into the time for making random reads. Now the `avrq-sz` maxes out. Now a single fio read requires more than one 'sequential low level reads' so `r/s` now increases steadily. Until the point of 16mb where each fio read equals 32 sequential reads at the block layer. This results in very high `r/s` and the corresponding `rKB/s` shows sequential-like bandwidths. So far so good! If you see the `bw` column, its doubling all the way from 1 byte to 512kb. Until 4kb block size this is caused by simply reading more from the 4k filesystem block that is already read anyway. From 4k to 512k, the doubling is caused due to the doubling of file system block size that is being read. You can see from 4k to 512k block size, the `bw` pretty much matches with `rKB/s`. But what the heck happened after 1MB block size?!?! `bw` has shot upto 1.3 GB/s, while rBK/s continues to be around 70MBps range. The linux page cache is causing this. If you see the `rKB/s` column, we are doing around 70MBps. We can read the entire 3GB file in `3000/70 = 42` seconds. For the rest 18 seconds, the requests are served through ram and the iops and bw shoots through the roof. Also observe that this is the first time that the file could be read entirely into the page cache. Because, for the previous run with `2^19` the value of rKB/s is around 50MBps. In 60 seconds, it just managed to (or missed to ) read `50*60sec = 3G` file. So we didnt observe cache effects for the previous run. After 2^20, the bw still keeps increasing, probably because we are filling up the page cache earlier in each run (due to increase in `rKB/s`) . Furthermore it seems like fio does a `drop-cache` to clear the cache before every run (which is good for us). Now observe the `iops` graph. After the spectacular shootup at 2^20, the iops keeps halving. This makes perfect sense because the requests are being served from ram. ram being truly random access, the bandwidth has to remain constant. So if you double the block size, the iops should halve. Sweet! 


Unexplained/TODO:
I tried to explain the `r/s` graph in more quantitative terms. If my theory holds, then the V shape from 2^16 to 2^23 is caused by seek_time + sequential_throughput.
i.e. to read a block of `x kb`, time taken should be `seek_time + sequential_throughput_sec_per_kb*x`
Now you can actually calculate `seek_time` and `sequential_throughput` with the values at 2^17 and 2^18

When you extrapolate it to other values, I get `2^19 = 85 r/s`, `2^20 = 107 r/s`, `2^21 = 123 r/s` and `2^22 is 133 r/s`. This doesnt quite match up with the observed values in the graph. Maybe some other cache is coming into effect here ?

### sync,read,sync=0,direct=0
This is another interesting graph where we observe quite a different phenomenon. First, let's consider the `util` column. We observe that until bs=7, the disk is actually underutilized. This means that until bs=7, the entire goddamn process is bottlenecked on CPU. Indeed, when I checked % cpu utilization through top, the CPU was at humming at 100%. Looking at the iops graph, it is constant until bs=7. We conclude that 900K iops is the theoritical maximum that the linux kernel can perform. So 1.1 microseconds per system call. Useful number to remember! 
Looking at the `r/s` graph, it is fairly simple. Until bs=7, values keeps doubling. Why? when we double the fio block size, iops being constant, the kernel can read data twice as fast and will thus issue disk reads twice as fast. After bs=8, the number of `r/s` have completely saturated. This is the time when the disk is 100% utilized and cpu/kernel/memory is no longer the bottleneck. The `rKB/s` is uninteresting since it is simply following `r/s` (because `avgrq-sz` is constant). But note that we get around 140 MBps for sequential throughput. 

Now lets tackle `iops`. We already explained the constant iops until bs=7. From bs=8, A couple of things are happening here. First note the `io` column. For bs=8, we have read 11GB of data, so in the middle of the 60 second run, the entire file was page-cached in memory and the rest of time was served purely from ram. So the reduction in iops is because for some fraction of the 60 second time, we are actually bottlenecked on hard disk. For subsequent values of bs, the fraction of time of hard-disk bottleneck remains constant (and hence the fraction of time cpu bottlenecked also remains constant) but in the cpu bottleneck phase, since the block size has doubled, iops will have to halve. Note that in the initial stages values after bs=7. i.e., for bs=8, 9, 10 the decrease in iops is less than half. This is because the system_call/kernel overhead is still the majority of time. As block size gets bigger, The time copying from kernel space to user space overwhelms the systemCall/kernel time, and we observe proper halving of iops (see iops values bs=15). This also explains why `bw` saturates after bs=15. It is caused because once kernel/systemCall time became negligible, the bandwidth is simply `iops*bs`. This remains true for all subsequent values of bs.

The story with `bw` is similar. Up until bs=7, the bw has exactly doubled, because fio was 100% CPU bottlenecked. Starting from bs=8, there is a component that cannot be increased (when bottleneck is hard-disk) and there is a component that can be doubled (when bottleneck is cpu and 1microsecond system call processing time). So the average increase is 1.64 times previous value

#### Quantitative explanation
Assume the following numbers:
* Time to make one system call irrespective of block size = 1.1 microseconds
* RAM-to-RAM copy bandwidth 4.6 GBps (i.e., to copy from kernel space to user space)

For bs=2^9, at the rate of 138 MBps disk read speed, the disk was busy for 3G/138MBps = 22.6 seconds. Number of fio io operations for the first 22.6 seconds= 3G/2^9 = 6291456.
For the next 60 - 22.6 = 37.4 seconds, requests were served purely from copying data from page cache to user space (RAM-to-RAM copy). Time for each io operation = 1.1 microseconds + 2^9 / 4.8GBps = 1.2 microseconds. So in 37.4 seconds, number of fio operations = 37.4 / 1.2 microseconds = 31.16 million fio operations. So net io operations = 31.16 million + 6291456 = 37458122. 
iops calculated over 60 seconds = 37458122/60 = 624302. This differs from actual value of 617759 by 1%.
The actual percentages of error using this method (starting from bs=512) is 
0.80, 3.64, 3.32, 9.78, 11.94, 13.33, 15.65, 15.38, 0.99, 10.13, 5.77, 3.85, 2.75, 3.17, 3.66, 12.44
Even with 15% error, its not too shabby i guess, in the face of other complications such as page faults and TLB misses

Unexplained:
The `avgrq-sz` seems to be stuck at 512 sectors. Why? we saw in the case of `libaio,randread,sync=0,direct=0` that `avgrq-sz` went upto 1024 sectors. 

explain the `bw` from 2^16 onwards

Quantitatively verify if the theories make sense. 

