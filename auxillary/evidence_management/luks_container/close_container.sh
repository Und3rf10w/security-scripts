#!/bin/bash

source /tmp/.lukscryptinfo
umount /mnt/$volume_name
cryptsetup luksClose $volume_name
if [ ! -z "$volume_name" ] then
	rmdir /mnt/$volume_name
fi
shred -z -n 5 -u -f /tmp/.lukscryptinfo
