Date: 2016-08-23 12:30 am
Tags: misc
Authors: Sharath Gururaj
Title: Notes about kafka metrics
disqus_identifier: notes-about-kafka-metrics

# Notes about kafka metrics

**Bytes in** is number of bytes from external producers only. It does not include, for example, the bytes read by followers during replication. So `bytes_in = message_produce_rate * average_message_size`

**Bytes out** includes data sent to follower also.