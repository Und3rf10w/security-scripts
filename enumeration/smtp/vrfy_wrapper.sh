#!/bin/bash

for host in $(cat smtp_hosts); do
	echo "Usernames VRFYed for $host"
	for name in $(cat namelist.txt); do
		./vrfy_enum.py $host $name |grep 250;
	done
done
