Date: 2021-09-20 10:30 pm
Tags: misc
Authors: Sharath Gururaj
Title: Notes on Postgres WAL and logical replication
disqus_identifier: my_blog

We are trying to implement change data capture (CDC) from several postgres databases and expose it as a stream of inserts/updates/deletes to any consumer. 

A couple of properties of all our tables, which makes the design much easier is:

- All tables have an immutable primary key (usually a UUID), although sometimes, the primary key may be a composite key. It allows us to "replay" rows over and over again, without worrying about duplicates, etc
- All tables also have audit columns (created_at, updated_at). It allows us to query changes since (say) yesterday and reingest the data using the immutable primary keys


Here are some practical requirements from any such CDC system.

- In case the destination crashes, we want to replay the changes from the last X days (assuming WAL logs are maintained)
- In case of master failover to replica, we want to "continue from where the master fell off", or at least, rewind back a couple of hours and replay the messages.
- We want to selectively choose what tables to replicate, and this set of tables might change. (typically, new tables will be added to the captured list)`
- The ability to perform parallel initial snapshot and streaming, and the ability to resume initial snapshot in case of error 

The *de facto* choice for CDC these days is debezium, which uses logical replication to expose a stream of changes. When practically trying to build such a system, we had a hard time figuring out how all the components fit together. The postgres and debezium docs are very good, but they have big gaps if you want to understand the systems well enough to architect a solution. So in this blog, we will cover the missing pieces that we figured out reading the source code. 

This article is meant to be read along with the available documentation of postgres logical replication and debezium documentation. As such, we will not cover introductory things like what is logical replication, etc. we will go straight to the points which we consider is not clear in the documentation. A really fantastic place to get background information is [https://www.interdb.jp/pg/](https://www.interdb.jp/pg/).

## Some implementation details of the postgres WAL mechanism 
As soon as queries execute `insert/delete/updates`, The generated `XLogRecords` are put in a shared memory called the **WAL Buffers**. There is a **WAL Writer** process that wakes up regularly and flushes the WAL Buffer to disk. Note that this writing happens even for potentially uncommited transactions. The fact that a transaction is rolled back is handled by simply marking the transaction in the `pg_xact` as `rolled_back`. There are two invariants that are maintained.

- All `XLogRecords` are flushed to disk at some point **before** the transaction is marked as committed
- When the WAL Writer kicks in, all `XLogRecords` **upto a specific LSN** are written. This means that **`XLogRecords` from different transactions can be intermixed freeley**. For example, the following is a valid sequence of records in the WAL File
````java
begin_tx1, begin_tx2, tx1_xlogrecord1, tx2_xlogrecord1, commit_tx1, commit_tx2
````

## Some implementation details of logical replication 
- On the server side, the replication slot primarily holds information about how much LSN the client has read so far.
- On the server side the flow of reading the logs is like this
````java
WalSender --> ReorderBuffer --> OutputPlugin (for example pgoutput)
````
- Each replication slot has its own WALSender process. 
- The output plugin free to do whatever it wants with the decoded `XLogRecords`. It may or may not send the changes over on the network to a remote peer. For example, there is a [SQL interface](https://www.postgresql.org/docs/10/logicaldecoding-example.html) which is a plugin which exposes the functionalities through a few SQL functions. 
- Any logical replication plugin must be associated with a replication slot to start doing the magic.
- pgoutput is one such plugin, that streams the changes over the network, with a well defined [protocol](https://www.postgresql.org/docs/current/protocol-logical-replication.html).
- On the client side, the WALReciever process understands the protocol of pgoutput, and converts the messages to SQL and replays it on the client.
- As with all output plugins, pgoutput also requires a replication slot. However, unlike other plugins, pgoutput requires another object called a *publication*. The publication is effectively nothing more than a list of tables that need to be captured. It is read only during the startup of streaming, or when we manually refresh a publication

Now we would like to point out a tricky implementation detail.
- On the server side, we saw that WAL files contain `XLogRecords` intermixed records from different transactions. However, when the changes appear on the client side, they are no longer intermixed. For example, suppose the WAL file on server looks like this:

````java
begin_tx1, begin_tx2, tx1_xlogrecord1, tx2_xlogrecord1, commit_tx1, commit_tx2
````

but the client sees the changes look like this:
````java
begin_tx1, tx1_xlogrecord1, commit_tx1, begin_tx2, tx2_xlogrecord1, commit_tx2
````

This magic is performed by the `ReorderBuffer` module pointed out above. Note that this component comes before the output plugins, so all output plugins behave this way. 

By now, you must be wondering that the only way to accomplish is to buffer the `XLogRecords` in memory until we encounter the commit record, and then emit all changes without intermix.

Well you are right. ReorderBuffer does exactly that. The astute observer will note that the amount of transaction record can grow big. Much bigger than available memory. Well, the ReorderBuffer infact has the capability to splill its data structures to disk to accomplish this de-intermix!

The pseudocode of ReorderBuffer is something like this
````java 
1. Maintain a datastructure recordMap::Map<txid, List<XLogRecords>
2. start reading the WAL
3. for each XLogRecord rec:
       a. recordMap.get(rec.txid).append(rec)
       b. if the list is bigger than threshold, spill to disk
       c. if rec==COMMIT, then emit all the changes of recordMap.get(rec.txid)
````

An important consequence of this "de-mixing" is that the LSN of records as seen by the client need not be in increasing order.
However, the following two invariants are still maintained
- LSNs of each transaction is ordered
- LSNs of commit messages are ordered

## Keeping track of progress of logical replication
Periodically, the client sends back heartbeat messages to server, which contain the following three lsns. 
- confirm_flush_lsn
- recieve_lsn
- apply_lsn

To understand these LSN, consider the client as a database. When it recieves a message, it performs the following steps
- recieve the lsn
- apply it to tables
- fsync and flush the changes

So each lsn corresponds to these steps. Usually, `recieve_lsn>apply_lsn>flush_lsn`

Of course, a client may not actually use three different steps. The most important of these is `flush_lsn`. It tells the server that lsns before this will no longer be required by the client and free to reclaim the space in WAL

## On server restart, from where does the server restart the WAL decoding?

The server keeps track of all three progress lsns. In particular the `flush_lsn`. So logically, one might think that on restart, this is the point from where the server will play back the WAL. However, the server persists the `flush_lsn` only at checkpoint, so it is entirely possible that the client may recieve duplicate entries on restart. It is upto the client to skip duplicates. Furthermore, one can actually specify the restart LSN during startup.

There is in fact another LSN called `restart_lsn` that is tracked by the server. We are not able to figure out the difference between `restart_lsn` and `flush_lsn`

## Some notes for architects

Q: How far can I go back and restart the streaming?<br/>
A: By cleverly controlling flush_lsn, you can control the amount of WAL retained on the server.

Q: How do we make sure server does not crash due to WAL locking up disk space due to inactive replication client<br/>
A: You can play with some postgres parameters, notably `wal_keep_size` and `max_slot_wal_keep_size`

Q: How do we get resumable and parallel initial snapshots?<br/>
A: refers to these links. [DDD-3](https://github.com/debezium/debezium-design-documents/blob/main/DDD-3.md) and [DbLog](https://arxiv.org/pdf/2010.12597v1.pdf)

Q: If the master fails-over to a replica, the LSNs will go out of sync. Do we need to resetup the entire snapshot?<br/>
A: Here's the idea:
- create a replication slot on the new primary (previously standby)
- issue a query like so `select * from mytable where updated_at > now()-2hrs`. Once it's done, start the streaming replication.
Assuming your primary keys are idempotent, you should be back in business

Q: How can we add or remove from the list of captured tables?<br/>
A: Since debezium reads pgoutput protocol, just alter the publication and restart debezium 

## Conclusion
Logical decoding is a very powerful tool in the data engineering toolkit. It opens up a host of possibilities. we hope this article fills in the gap left in official documentation and enables architects to design effective CDC systems.

