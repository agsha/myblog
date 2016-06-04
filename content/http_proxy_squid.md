Date: 2016-03-02 10:20
Tags: regex
Authors: Sharath Gururaj
Title: http and https proxy with squid
disqus_identifier: squid_proxy


### On the client machine
* Find out the client subnet of the form `10.34.44.0/22`. To do that, on the client machine, run `/sbin/ifconfig` to find out the       ip address and subnet mask. with these two pieces of info, you can calculate the CIDR [here](http://www.subnet-calculator.com/cidr.php)
* export variables: 
  ````
  export http_proxy=http://client.ip.ad.ress:port/
  export https_proxy=http://client.ip.ad.ress:port/
  ````
### Caveat
if you run sudo, make sure the variables are exported in root

### On the proxy machine
* Install squid: `sudo apt-get install squid`. 
* change /etc/squid/squid.conf to add these lines
   ````
   acl wormhole src 10.34.44.0/22 # the client subnet who need the proxy
   http_access allow wormhole # wormhole is just a name
   icp_access allow wormhole
   ````
  
* restart squid `sudo /etc/squid/squid.conf restart`

And thats it! `curl -L www.google.com` (`-L` to follow redirects) will work.

I needed this for `pip`. With my setup, I can do `sudo export <blah>;export<blah>;pip install <package>`. 

FYI, my squid version is
````
[sharath.g@d42-a-0003 /home/sharath.g]$ dpkg -s squid
Package: squid
Status: install ok installed
Priority: optional
Section: web
Installed-Size: 1864
Maintainer: Luigi Gangitano <luigi@debian.org>
Architecture: amd64
Version: 2.7.STABLE9-4.1+deb7u1
Replaces: squid-novm
Depends: libc6 (>= 2.7), libcomerr2 (>= 1.01), libdb5.1, libgssapi-krb5-2 (>= 1.10+dfsg~), libkrb5-3 (>= 1.6.dfsg.2), libldap-2.4-2 (>= 2.4.7), libpam0g (>= 0.99.7.1), netbase, adduser, logrotate (>= 3.5.4-1), squid-common (>= 2.7.STABLE9-4.1+deb7u1), lsb-base (>= 3.2-14), perl-modules
Pre-Depends: debconf (>= 1.2.9) | debconf-2.0
Suggests: squidclient, squid-cgi, logcheck-database, resolvconf (>= 0.40), smbclient, winbind
Conflicts: sarg (<< 1.1.1-2), squid-novm
Conffiles:
 /etc/init.d/squid 04af7c1f2d27c35db0200679fbc9bdbe
 /etc/logrotate.d/squid 0dd1fea0f842a58f538408754e747311
 /etc/resolvconf/update-libc.d/squid f8d0ffa84ddd982f32da05cb61bc479e
Description: Internet object cache (WWW proxy cache)
 This package provides the Squid Internet Object Cache developed by
 the National Laboratory for Applied Networking Research (NLANR) and
 Internet volunteers.
Homepage: http://www.squid-cache.org/

````
