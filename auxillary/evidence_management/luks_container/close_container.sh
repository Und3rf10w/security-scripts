#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This must be ran as root"
	exit 1
fi

source /tmp/.lukscryptinfo
umount /mnt/$volume_name
cryptsetup luksClose $volume_name
if [ ! -z "$volume_name" ] then
	rmdir /mnt/$volume_name
fi
shred -z -n 5 -u -f /tmp/.lukscryptinfo
