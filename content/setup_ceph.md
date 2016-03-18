Date: 2016-02-07 10:20
Tags: ceph
Authors: Sharath Gururaj
Title: Setting up a ceph cluster

The instructions [here](http://docs.ceph.com/docs/hammer/install/manual-deployment/) mostly work. Except that the `ceph.conf` file  given there doesnt work. Because, when I issue `sudo /etc/init.d/ceph start mon.node1` in the end, It expects a section in `ceph.   conf` called `[mon.node1]`


Furthermore, to launch a radosgw instance, you *need* to have a section in your host file called `client.rgw.<some_name>` and your  keyring should have a corresponding key section called  `client.rgw.<some_name>` and you should have imported that key into ceph    via ` sudo ceph auth import -i /etc/ceph/<keyring_file>`.

**All the three names must match: the one in ceph.conf, in the keyring and in `ceph auth list`**

Oh, and yeah, do **NOT** put a line like this in your `ceph.conf`:
````sh
rgw data = /var/lib/ceph/radosgw/ceph-rgw.prod-d42sa-rgw-a-287004
````
If you do, you'l get weird messages like 

> Couldn't init storage provider (RADOS)

and you'll go crazy trying to debug it.

So the working `ceph.conf` with comments is: 
````sh
[global]
fsid = a7f64266-0894-4f1e-a635-d0aeaca0e993 #anything random, generated from uuidgen
auth cluster required = cephx
auth service required = cephx
auth client required = cephx
osd journal size = 1024
filestore xattr use omap = true
osd pool default size = 2 
osd pool default min size = 1 
osd pool default pg num = 333 
osd pool default pgp num = 333 
osd crush chooseleaf type = 1 
# useful for debugging
[mon]
  debug mon = 20
[osd]
  debug osd = 20
[rgw]
  debug rgw=20
[mon.node1] # as many sections as monitors
  host = dev-d42sharath1-mon-a-0001-389313 #This NEEDS to be the actual hostname donno for what reasons
  mon addr = 10.33.29.199 # needs to be the actual address.
[client.rgw.foo]
    host = dev-d42sharath1-rgw-a-0001-389309
    keyring = /etc/ceph/ceph.client.rgw.keyring
    log file = /var/log/radosgw/client.radosgw.gateway.log
    rgw frontends = civetweb port=80
    rgw print continue = false

````

