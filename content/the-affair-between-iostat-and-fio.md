Date: 2016-07-02 04:20 pm
Tags: misc
Authors: Sharath Gururaj
Title: The affair between iostat and fio 
disqus_identifier: c_ide


In the following analysis, I'm going to assume you already know what `fio` and `iostat` is (I'm too lazy to write it down, and there are better articles out there). This post merely explains the relationship between the numbers

### fio output

```
[sharath.g@prod-d42ar-osd-a-00050-409388 /home/sharath.g]$ sudo fio --name=global --bs=4k --ioengine=libaio --iodepth=1 --runtime=120 --time_based --size=3G --group_reporting --disable_lat=1 --disable_clat=1 --disable_slat=1 --clat_percentiles=0  --filename=/var/lib/ceph/osd/ceph-153/fio/my_journal  --name=regular_read --rw=randread
regular_read: (g=0): rw=randread, bs=4K-4K/4K-4K, ioengine=libaio, iodepth=1
2.0.8
Starting 1 process
Jobs: 1 (f=1): [r] [100.0% done] [1112K/0K /s] [278 /0  iops] [eta 00m:00s]
regular_read: (groupid=0, jobs=1): err= 0: pid=501549
  read : io=126112KB, bw=1050.1KB/s, iops=262 , runt=120001msec
    bw (KB/s)  : min=  785, max= 1338, per=100.00%, avg=1051.79, stdev=91.21
  cpu          : usr=0.19%, sys=0.96%, ctx=19643, majf=0, minf=21
  IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued    : total=r=31528/w=0/d=0, short=r=0/w=0/d=0

Run status group 0 (all jobs):
   READ: io=126112KB, aggrb=1050KB/s, minb=1050KB/s, maxb=1050KB/s, mint=120001msec, maxt=120001msec

Disk stats (read/write):
  vdb: ios=19591/0, merge=0/0, ticks=118660/0, in_queue=118644, util=99.08%
```

### iostat output

````
[sharath.g@prod-d42ar-osd-a-00050-409388 /home/sharath.g]$ iostat -x  -d 2 /dev/vdb
Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
vdb               0.00     0.00  165.00    0.00   660.00     0.00     8.00     0.99    6.02    6.02    0.00   6.02  99.40
````

