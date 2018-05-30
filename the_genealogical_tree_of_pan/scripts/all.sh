#!/bin/bash
> book.md

for MD in "	\
	src/system/install.md src/system/readme.md  	\
	src/system/locale_and_timezone.md		\
	src/system/date_and_time.md			\
    	src/system/users_and_group.md			\
    	src/system/networking.md			\
    	src/system/nettools.md				\
	src/system/nettools/ping.md			\
	src/system/nettools/traceroute.md		\
	src/system/nettools/netstat.md			\
	src/system/nettools/route.md			\
	src/system/nettools/ss.md			\
	src/system/nettools/ip.md			\
	src/system/nettools/host.md			\
	src/system/nettools/nslookup.md			\
	src/system/nettools/nc.md			
	"
do
	cat $MD >> book.md
done
