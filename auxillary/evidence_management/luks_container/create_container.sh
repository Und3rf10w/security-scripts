#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root" 
	exit 1
fi

# Script will create the encrypted LUKS container, and format it with ext4
read -p "What size should the container be in MB? (512): " container_size
read -p "Where should we store the container? (/root/container): " container_path
dd if=/dev/urandom of=$container_path bs=1M count=$container_size

cryptsetup -y luksFormat $container_path
cryptsetup -y luksOpen $container_path somerndvolume

mkfs.ext4 -j /dev/mapper/somerndvolume
echo "Container is formatted with ext4"

cryptsetup luksClose somerndvolume
