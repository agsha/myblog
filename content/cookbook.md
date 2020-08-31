Date: 2020-08-31 00:22 pm
Tags: misc
Authors: Sharath Gururaj
Title: Cookbook
disqus_identifier: cookbook

This article captures cookbooks or recipes that I don't use frequently enough to remember, but still use it enough to be painful to google from scratch every time I use it. Its a bunch of totally unrelated stuff that is too short to put as a blog article on its own. Hopefully, you'll find the table of contexts helpful to navigate.
(the links are not working yet :( )


# <a name="table-of-contents" href="#table-of-contents">Table of contents</a>

<!-- toc -->- [Table of contents](#table-of-contents)
- [Julia Arrays](#julia-arrays)
- [Anaconda dont start at shell](#anaconda-dont-start-at-shell)
- [How to mount samba folder in ubuntu](#how-to-mount-samba-folder-in-ubuntu)
- [How to use du to search for hidden folders](#how-to-use-du-to-search-for-hidden-folders)
- [Sublime text keyboard shortcuts](#sublime-text-keyboard-shortcuts)
- [Making Nomachine nx work on amazon aws ec2](#making-nomachine-nx-work-on-amazon-aws-ec2)
- [Remote desktop to raspberry pi](#remote-desktop-to-raspberry-pi)
- [Echo server with netcat ](#echo-server-with-netcat)
- [Mounting a disk on GCP](#mounting-a-disk-on-gcp)
- [Describe type of command](#describe-type-of-command)
- [Linux Networking](#linux-networking)
- [Postgres](#postgres)
- [Intellij Shortcuts](#intellij-shortcuts)
- [Bash shortcuts](#bash-shortcuts)
- [How to setup a new linux machine](#how-to-setup-a-new-linux-machine)
- [Python regex recipes ](#python-regex-recipes)
- [Vim one liners and shortcuts](#vim-one-liners-and-shortcuts)
- [Cscope for linux ](#cscope-for-linux)
- [Cscope for ceph](#cscope-for-ceph)
- [Building linux](#building-linux)
- [Using Ftrace to trace linux functions](#using-ftrace-to-trace-linux-functions)
- [How to build linux on one machine and deploy on another](#how-to-build-linux-on-one-machine-and-deploy-on-another)
- [JeMalloc ](#jemalloc)
- [Objdump](#objdump)
- [Installing latest version of cmake](#installing-latest-version-of-cmake)
- [Getting honest profiler to work](#getting-honest-profiler-to-work)
- [GCC important options](#gcc-important-options)
- [Eli bendersky static linking summary](#eli-bendersky-static-linking-summary)
- [Eli bendersky load time linking summary](#eli-bendersky-load-time-linking-summary)
- [Eli bendersky x32 PIC linking summary](#eli-bendersky-x32-pic-linking-summary)
- [Linux Interrupt Handling](#linux-interrupt-handling)
- [HDFS proxy user setting](#hdfs-proxy-user-setting)
- [Http proxy with squid](#http-proxy-with-squid)
- [kafka metrics](#kafka-metrics)
<!-- tocstop -->


# <a name="julia-arrays" href="#julia-arrays">Julia Arrays</a>
 * tabs or spaces: concat to the right
 * semicolon or newline: concat to the bottom 
 * one dimensional arrays are considered as column vectors for concatenation purposes

# <a name="anaconda-dont-start-at-shell" href="#anaconda-dont-start-at-shell">Anaconda dont start at shell</a>
If you'd prefer that conda's base environment not be activated on startup, 
````bash
conda config --set auto_activate_base false
````

# <a name="how-to-mount-samba-folder-in-ubuntu" href="#how-to-mount-samba-folder-in-ubuntu">How to mount samba folder in ubuntu</a>
````bash
sudo mount -t cifs -o user=sharath //192.168.29.28/HOMEPI /mnt/pi
````

# <a name="how-to-use-du-to-search-for-hidden-folders" href="#how-to-use-du-to-search-for-hidden-folders">How to use du to search for hidden folders</a>
````bash
du -schx .[!.]* *
````
To exclude other mount points use `--exclude`

# <a name="sublime-text-keyboard-shortcuts" href="#sublime-text-keyboard-shortcuts">Sublime text keyboard shortcuts</a>
Open any file `ctrl-p`
Open any command `ctrl-shift-p`
Close tab: mac `cmd+w`
Linux `ctrl-shift-w`
Jump back `alt -` 
forward `alt +` 

# <a name="making-nomachine-nx-work-on-amazon-aws-ec2" href="#making-nomachine-nx-work-on-amazon-aws-ec2">Making Nomachine nx work on amazon aws ec2</a>
First, download the nx package from nomachine and `dpkg -i` the package
The software is installed in `/usr/NX`
We have to first disable password login and only use certificate login. To do this, edit the file `vim /usr/NX/etc/server.config` and add this line. After this, restart the nx server `/usr/NX/bin/nxserver --restart`
Verify that password login does not work
For resolution, the key idea is that there should be no x server running already on the machine. If there is no x server, then nx will create its own, and by default try to match the client resolution, which is what we want. Unfortunately, when we install gnome desktop, it automatically changes the systemd runlevel to graphical.target which means systemd will spawn gdm and an xserver /usr/lib/xorg/Xorg (hope you dont get into wayland and shit). So we have to change the default systemd target to shell mode, which can be done by `sudo systemctl set-default multi-user.target`* 
And thats it, nx should automatically try to match client resolution if client is running in full screen mode!

Sometimes, you will see a black screen when you login, to solve this
````bash
sudo service gdm stop
/usr/NX/bin/nxserver --restart
````

# <a name="remote-desktop-to-raspberry-pi" href="#remote-desktop-to-raspberry-pi">Remote desktop to raspberry pi</a>
We will use real vnc. From terminal, ssh to raspberry pi. On the pi run
`vncserver -geometry 1920x1080`

From the client, run vncviewer from real vnc and login. You have to do this every time you want to login

# <a name="echo-server-with-netcat" href="#echo-server-with-netcat">Echo server with netcat </a>
Server
`ncat -e /bin/cat -k  -l 8888 <ip>`

Client 
`telnet ip 8888`

# <a name="mounting-a-disk-on-gcp" href="#mounting-a-disk-on-gcp">Mounting a disk on GCP</a>
````bash
sudo lsblk
sudo mkdir -p /mnt/disks/sdb
sudo cp /etc/fstab /etc/fstab.backup
sudo blkid /dev/sdb
In /etc/fstb
UUID=[UUID_VALUE] /mnt/disks/[MNT_DIR] ext4 discard,defaults,nofail 0 2
Sudo mount -a 
````


# <a name="describe-type-of-command" href="#describe-type-of-command">Describe type of command</a>
`type ls`

# <a name="linux-networking" href="#linux-networking">Linux Networking</a>
* **Netfilter**: linux component which has various hooks for network packet manipulation
The netfilter hooks are exposed through various  userspace programs: notably 

* **Iptables** : which is the userspace interface to linux firewall, (firewall here simply means configuring netfilter according to some rules), nat mangling etc 
 
* **Subnetting/CIDR** : CIDR splits 32 bit ipv4 addresses into two parts: left part is network part. Right part is host part. This act is called subnetting. `0.0.0.0/24` Here 24 means, the network part (left part) is 24 bits. The host part (right part is 32-24 = 8) bits. Usually in large companies different networks are indeed different networks. I.e., we need routing between two subnets. With a single (sub)network, there is no need for routing (works like lan)
* **Network interfaces**: on the linux level, they are network devices, with a device driver. They get a packet trhough hard_start_xmit() and they can do whatever they want with it. See this for a good example
* **Bridge**: when referring to a hardware device it is a connector at L2. i.e., it learns mac addresses and forwards packets from one network to another switch is also essentially the same thing
* **Linux software bridge device**:  is a software network_interface which acts like a bridge between two other network interfaces

# <a name="postgres" href="#postgres">Postgres</a>
To create a data directory, first 
````bash
mkdir -p /path/to/data
chown postgres  /path/to/data
Sudo -u postgres /usr/lib/postgresql/11/bin/Initdb -D /path/to/data
vim /etc/postgresql/11/main/postgresql.conf #and modify the data_dir
````
To make postgres listen to remote connections in the same file:
`listen_addresses = '*'`

`vim /etc/postgresql/11/main/pg_hba.conf `
Add this line (probably give stronger restrictions)
````text
host    all             all             0.0.0.0/0            md5
````

Restart postgres. There are several ways. One of these should work:
````
    Sudo service postgresql restart
Or 
    pg_ctlcluster 12 main start
Or 
pg_ctl -D /usr/local/var/postgres start
Or
    /usr/lib/postgresql/10/bin/pg_ctl -D /etc/postgresql/10/main -l logfile start
Or
   sudo systemctl start postgresql@10-main
````

Create users by first logging in 
````bash
sudo -u postgres psql
create user sharath with encrypted password 'foo';
ALTER USER sharath WITH SUPERUSER;
create database sharath;

#To enable the logs in /etc/postgresql/11/main/postgresql.conf
log_destination = 'csvlog'
logging_collector = on
log_rotation_age = 0d
log_statement = 'all'
````
To view the logs
`sudo grep SQLEditor /var/lib/postgresql/12/main/log/* |grep -v pg_catalog | grep -v SHOW | grep -v current_schema`

# <a name="intellij-shortcuts" href="#intellij-shortcuts">Intellij Shortcuts</a>
* Ctrl+shift+enter to complete statement after code completion. Its pretty magical. 
* Alt+j to select all instances
* Tab after ctrl-space overwrites rather than insert
* Ctrl+alt-l to reformat whole file or selections
* Ctrl+shift+i to see the definition (code) for the method
* F2 to go to next highlighted error
* F4 go to definition
* Ctrl-f12 to see the file structure
* Ctrl+shift+numpad- collapse all


# <a name="bash-shortcuts" href="#bash-shortcuts">Bash shortcuts</a>
* Alt-B back one word
* Alt-f forward one word
* Ctrl-w delete back one word
* alt-D delete till end of word
* Ctrl-U delete to start of line
* Ctrl-k delete to end of line


# <a name="how-to-setup-a-new-linux-machine" href="#how-to-setup-a-new-linux-machine">How to setup a new linux machine</a>
First, login as root. Here nm> means new machine and local> means laptop
````bash
nm> 
adduser -u 1001 sharath;
usermod -aG sudo sharath
su - sharath
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
<create a new key>
<copy your localhost id_rsa.pub into clipboard>
vim /home/sharath/.ssh/authorized_keys 
<paste your id_rsa.pub and exit vim>
chmod 644 /home/sharath/.ssh/authorized_keys
echo 'sharath ALL=(ALL) NOPASSWD: ALL' | sudo tee /etc/sudoers.d/sharath
sudo chmod 0440 /etc/sudoers.d/sharath
````

IMPROVED (scriptable)
````bash
First, copy your public key to tmp on nm, like so
scp ~/.ssh/id_rsa.pub root@<new_ip>:/tmp/ak 

Login to the new box as root and do the following
adduser --disabled-password --gecos ‘’ sharath
usermod -aG sudo sharath
su - sharath
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
exit
cp /tmp/ak /home/sharath/.ssh/authorized_keys
chmod 644 /home/sharath/.ssh/authorized_keys
echo 'sharath ALL=(ALL) NOPASSWD: ALL' | sudo tee /etc/sudoers.d/sharath
sudo chmod 0440 /etc/sudoers.d/sharath
rm /tmp/ak
````

Bob should be your uncle

# <a name="python-regex-recipes" href="#python-regex-recipes">Python regex recipes </a>

* \s whitespace
* \S non whitespace
* \d only digits
* \D non digits
* \w alphanumeric [a-zA-Z0-9_]
* \W non-alphanumeric
* \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} ip regex

groups enclose in (), numbered from x.group(1)
named groups like this `(?P<name) access with x.group("name")`
````python
r = re.compile(regexStr)
for x in r.finditer(str):
	x.group(1)
	x.group("name")

r = re.compile(r"(blue|red)")
r.sub(lambda m: str(len(m.group())), "blue socks and red shoes")
````

prints `4 socks and 3 shoes`

validate a regex on https://regex101.com/

# <a name="vim-one-liners-and-shortcuts" href="#vim-one-liners-and-shortcuts">Vim one liners and shortcuts</a>
* gd will go to local definition
* gD will go to global definition 
* ,c<space> toggle comment
* <ctrl>]  goes to a tag
* <ctrl>o (“old” comes back from a jump)
* <ctrl> i (opposite of <ctrl>o
* Split window ctrl-w v or o
* Scroll up/down, keeping your cursor in its row
* One line
* Ctrl+Y → Move viewport down
* Ctrl+E → Move viewport up (Extra lines)
* Column select <ctrl>v 
* Go to beginning of function (go to { in first column: needs coding convention) [[ 
* End of function ]]
* Beginning of code block: [{ this one should work better with messed up coding convention

# <a name="cscope-for-linux" href="#cscope-for-linux">Cscope for linux </a>
To apply debian patches use 
````bash
export LNX=/home/sharath/os/linux/linux-5.4.0
quilt push -a 
find  $LNX  -path "$LNX/arch/*" ! -path "$LNX/arch/x86*" -prune -o  -path "$LNX/include/asm-*" ! -path "$LNX/include/asm-i386*" -prune -o  -path "$LNX/tmp*" -prune  -path "$LNX/Documentation*" -prune -o  -path "$LNX/scripts*" -prune -o    -path "$LNX/drivers*" -prune -o   -path "$LNX/.pc/*" -prune -o  -path "$LNX/debian/*" -prune -o   -path "$LNX/sound/*" -prune -o    -name "*.[chxsS]" -print > kernel.cscope

cscope -q -R -b -i cscope.files
````

In vim
````text
:cs f g <foo> goto definition of foo
:cs f s <foo> find this symbol
:cs f t <foo> find this string
<ctrl>\ s on a word, find this symbol and so on
````

# <a name="cscope-for-ceph" href="#cscope-for-ceph">Cscope for ceph</a>
````bash
find /mnt/disks/sdb/ceph-pristine -type f -and \( -name "*.c" -o -name "*.h" -o -name "*.cc" -o -name "*.cpp" -o -name "*.hh" \) > zoo.cscope
cscope -q -R -b -i zoo.cscope 
````

# <a name="building-linux" href="#building-linux">Building linux</a>
You can get the linux source from 
`apt-get source linux-image-unsigned-$(uname -r)`

You can get the config file from 
`cp /boot/config-5.4.0-26-generic .config`
To install dependencies

````bash
sudo apt-get install libncurses-dev flex bison openssl libssl-dev dkms libelf-dev libudev-dev libpci-dev libiberty-dev autoconf
sudo apt-get build-dep linux linux-image-$(uname -r)

make ARCH=x86 EXTRAVERSION=-SS -j14 && make -j14 ARCH=x86 EXTRAVERSION=-SS install && make -j14 ARCH=x86 EXTRAVERSION=-SS modules_install; echo "------------------------- DONE --------------------------------"
rm /boot/initrd.img-3.16.43-SS
update-initramfs -c -k 3.16.43-SS
update-grub
````

# <a name="using-ftrace-to-trace-linux-functions" href="#using-ftrace-to-trace-linux-functions">Using Ftrace to trace linux functions</a>
````bash
echo 1 | sudo tee  /sys/kernel/debug/tracing/tracing_on
And then use brendan greggs perf-tools
sudo ./funcgraph -D  ext4_readpages | sudo tee /mnt/tmpfs/write
sudo ./funcgraph -Dp 51985  ext4_readpages | sudo tee /mnt/tmpfs/write
````

# <a name="how-to-build-linux-on-one-machine-and-deploy-on-another" href="#how-to-build-linux-on-one-machine-and-deploy-on-another">How to build linux on one machine and deploy on another</a>
Use “building linux” to build linux on one machine A. Suppose you want to install it on machine B
On machine B
````bash
Mkdir -p ~/kernel/boot
Mkdir -p ~/kernel/modules
````

On machine A
````bash
tar -cvzf ~/modules /lib/modules/3.16.43-SS
scp -r *SS* <B>:~/kernel/boot
scp ~/modules <B>:~/kernel/modules/
````

On machine B:
````bash
Cd ~/kernel/modules
tar -xvzf modules
sudo mv ~/kernel/modules/3.16.43-SS /lib/modules/
sudo cp ~/kernel/boot/* /boot/
sudo rm /boot/initrd.img-3.16.43-SS
sudo update-initramfs -c -k 3.16.43-SS
sudo update-grub


#And… reboot!
Sudo reboot now
````

# <a name="jemalloc" href="#jemalloc">JeMalloc </a>
Do a git clone.
````bash
./autogen.sh 
./configure --enable-prof --enable-stats --enable-debug
Make


[sharath.g@osboxes /home/sharath.g/code/jemalloc]$ tree lib 
lib
├── libjemalloc.a
├── libjemalloc_pic.a
├── libjemalloc.so -> libjemalloc.so.2
└── libjemalloc.so.2

#To generate the profile:
(reverse-i-search)`java': rm jeprof*; rm /tmp/prof.gif; MALLOC_CONF=prof:true,lg_prof_sample:0,lg_prof_interval:25 LD_PRELOAD=${JEMALLOC_PATH}/lib/libjemalloc.so.2 java -Xmx1096m -cp  '/home/sharath.g/diskbench/:/home/sharath.g/diskbench/*' sha.Memory; ls jeprof*; ~/code/jemalloc/bin/jeprof --show_bytes --gif `which java` jeprof*.heap > /tmp/prof.gif 
````

If you’ve compiled jemalloc on some other machine and copied it to this machine, youget teh error Can't exec "objdump": No such file or directory at /home/sharath.g/jemalloc/bin/jeprof line 4459.
Then objdump is 
Jemalloc what is active, dirty (unused), resident, total memory, allocated, mapped?
Allocated = sum of all malloc arguments that has not been freed 
Active .. multiple of page size.. Total bytes in pages that have at least one byte of allocated memory
Resident: active + metadata 
Mapped: multiple of chunk size. Total chunks that have one byte of allocated 
See that man pages for a clear explanation.

# <a name="objdump" href="#objdump">Objdump</a>
````bash
objdump -drSt hello.o
-d dissasemble
-r show relocation info inline
-S show C source code
-t show symbol table
````

# <a name="installing-latest-version-of-cmake" href="#installing-latest-version-of-cmake">Installing latest version of cmake</a>
Either apt-get install cmake or get it from here
https://cmake.org/download/
https://cmake.org/files/v3.8/cmake-3.8.0-rc4-Linux-x86_64.sh and run it

# <a name="getting-honest-profiler-to-work" href="#getting-honest-profiler-to-work">Getting honest profiler to work</a>
Installing it: 
If you’re lucky, you can download it and it works http://insightfullogic.com/honest-profiler.zip

Otherwise you need to build it. To build it, if you get weird errors, you might need to get latest version of Cmake, and then build it. You need build/libagent.so

Start the java program with       
`-agentpath:$HONEST_PROFILER_HOME/liblagent.so=host=localhost,port=4242,logPath=/grid/1/log/hadoop-yarn/yarn/honest-profiler.hpl`

Start and stop profiling with 
````bash
 echo start | nc localhost 4242
 echo stop | nc localhost 4242
````

Collapse the stacks with `java -cp $HONEST_PROFILER_HOME/honest-profiler.jar com.insightfullogic.honest_profiler.ports.console.FlameGraphDumperApplication netty.hpl netty.cstk`


# <a name="gcc-important-options" href="#gcc-important-options">GCC important options</a>
The linker `ld` takes as input .c files, .o files, .so files and can output an executable or a shared library.
The linker does not output static library. You can simply use ar for it

Gcc important options
-l mylib 
Look for a library called libmylib.{a, so}
But if both are present, will it choose .a or .so (it chooses .so) if you want to link an .a file, specify it directly on the command line. Or specify -static so it will choose .a even for libc 

Which directories to look in ?
-L dir is the answer

-i dir is for searching include files 
-include file
Is as if file was #included in source code in the first line. 

So basically `-L dir -l mylib -I dir -include files `

When creating an executable:
You cannot link a shared library statically by giving it on the command line (to create an executable) even if you give on command line, it still links it as  a shared library (as if you had given -L. -lxxx)
Or you cannot link a static library in a shared way by using -L and -l options (to create an executable)(you can but it will be taken as static, even if the static library is named libxx.so) 

Static libraries can be linked (statically) by specifying them as input files to gcc. Remember: static libraries are just a bunch of .o files 
You cannot skip specifying a shared library while linking to create an executable (although, technically they are not needed)  all variables must be resolved, which means that all shared libraries have to be specified (strictly not required, i guess its a sanity check) this has the effect of  listing in the executable as a dependency 	

For `LD_PRELOAD` to work, you have to specify -Wl,-soname,libml.so while having created that shared library this name is hardcoded into the so as its name, and this is the name that the linker looks at while loading the executable, not the file name of the .so

# <a name="when-creating-a-shared-library:" href="#when-creating-a-shared-library:">When creating a shared library:</a>
All object files must be compiled with -fpic
All ar files must have .o files which have been compiled with -fpic
If you specify multiple .so on command line, they will be combined into 1 .so as expected, with references resolved internally 
If a dependency is unmet (by not specifying some libraries at all) it is defined as undefined but linking succeeds
If a dependency is met by -L. -lxxx then it is undefined in the .so but that lib is listed as a dependency

# <a name="eli-bendersky-static-linking-summary" href="#eli-bendersky-static-linking-summary">Eli bendersky static linking summary</a>
Static linking algorithm perfectly explained in http://eli.thegreenplace.net/2013/07/09/library-order-in-static-linking
Some important points
* An object file both exports and imports symbols 
* individual object files specified on cmd line are always linked
* static libraries (ar) libraries serve only to provide a list of object files, and an object file in a library is linked only if it satisfies some current unmet dependency 

# <a name="eli-bendersky-load-time-linking-summary" href="#eli-bendersky-load-time-linking-summary">Eli bendersky load time linking summary</a>

Summary of load time linking as specified in http://eli.thegreenplace.net/2011/08/25/load-time-relocation-of-shared-libraries

Some gotchas: 
* Call operands are rip relative, but mov operands are absolute. In x86_64, there is a new addressing called RIP relative where any operand can be RIP relative.
* If a shared variable in a .so is referenced from the main executable, then that shared variable will go into the main executable, since the main executable is not relocatable. 
* what about a shared function in a .so referenced from main executable? The article does not mention it, but i imagine the functionality is similar. I.e. put the address of the function in the main program during load time and then call it.

Basically the address where a shared library is loaded is unknown
The static linker generates .so as if the shared library is loaded at 0x0 (logical)
The linker tells the offset of each variable in the file. 
The loader will add this offset to the load address to get the real address
The linker also populates a list where the real address has to be patched into the code. 
The loader will then patch the addresses in
Thats it.


# <a name="eli-bendersky-x32-pic-linking-summary" href="#eli-bendersky-x32-pic-linking-summary">Eli bendersky x32 PIC linking summary</a>

http://eli.thegreenplace.net/2011/11/03/position-independent-code-pic-in-shared-libraries

Instead of direct patching in the code, the real addresses of shared variables are stored in a GOT table in the data section. 
For mov operands, x32 does not support rip relative addresses, so there is a hack to get current rip address, then add the offset of the got table, and thus get the address of the variable

For call instructions, they are still using the hack but call supports rip relative addressing. So not sure what is happening,




# <a name="linux-interrupt-handling" href="#linux-interrupt-handling">Linux Interrupt Handling</a>
Peripheral devices pass interrupt to the interrupt controller (8259) which then passes it to processor on a given interrupt line.
An Interrupt line can be shared by multiple devices. To detect which device raised the interrupt, the linux interrupt handler iterates through all registered handlers on that line which then checks if that device raised the interrupt.
When an interrupt is raised, the processor disables all interrupts (on the local processor). 
The linux handler reenables interrupts (unless a flag was set while registering the handler) but disables the interrupt line (so none of the devices sharing can raise another interrupt) and calls the handler. For this reason, an interrupt handler need not be re-entrant. 
An interrupt handler cannot sleep/block because there is no “process” to sleep or block. (theoretically, the process can be considered to be the process that was interrupted but seems like a design decision to not let interrupt handlers sleep or not associate interrupt handlers with a process.

# <a name="hdfs-proxy-user-setting" href="#hdfs-proxy-user-setting">HDFS proxy user setting</a>
In addition to the modifications in core-site.xml we need to create the user and (add it to a group (?)) on the namenode. Even this is not working. It looks like the user needs to be added on the datanodes too. Is this true?
The logs from namenode are like this: 
````text
2017-06-05 11:48:27,271 INFO  ipc.Server (Server.java:doRead(850)) - Socket Reader #1 for port 8020: readAndProcess from client 10.32.10.3 threw exception [org.apache.hadoop.security.authorize.AuthorizationException: Unauthorized connection for super-user: hue from IP 10.32.10.3]
The ip 10.32.10.3 is a datanode.
````

# <a name="http-proxy-with-squid" href="#http-proxy-with-squid">Http proxy with squid</a>
### On the client machine
* Find out the client subnet of the form `10.34.44.0/22`. To do that, on the client machine, run `/sbin/ifconfig` to find out the       ip address and subnet mask. with these two pieces of info, you can calculate the CIDR [here](http://www.subnet-calculator.com/cidr.php)
* export variables: 
  ````text
  export http_proxy=http://client.ip.ad.ress:port/
  export https_proxy=http://client.ip.ad.ress:port/
  ````
### Caveat
if you run sudo, make sure the variables are exported in root

### On the proxy machine
* Install squid: `sudo apt-get install squid`. 
* change /etc/squid/squid.conf to add these lines
   ````text
   acl wormhole src 10.34.44.0/22 # the client subnet who need the proxy
   http_access allow wormhole # wormhole is just a name
   icp_access allow wormhole
   ````
  
* restart squid `sudo /etc/squid/squid.conf restart`

And thats it! `curl -L www.google.com` (`-L` to follow redirects) will work.

I needed this for `pip`. With my setup, I can do `sudo export <blah>;export<blah>;pip install <package>`. 

FYI, my squid version is
````text
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

# <a name="kafka-metrics" href="#kafka-metrics">kafka metrics</a>

**Bytes in** is number of bytes from external producers only. It does not include, for example, the bytes read by followers during replication. So `bytes_in = message_produce_rate * average_message_size`

**Bytes out** includes data sent to follower also.