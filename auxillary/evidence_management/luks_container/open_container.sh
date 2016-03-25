#!/bin/bash
# opens the luks container

if [[ $# -eq 0 ]]; then
	echo "USAGE: $0 -f </path/to/container> -n <volume name to use>"
	exit 0
fi

while [[ $# > 1 ]] 
do
	key="$1"
	case $key in
		-f)
		container_path="$2"
		shift;;
		-n)
		volume_name="$2"
		shift;;
		*)
		echo "USAGE: $0 -f </path/to/container> -n <volume name to use>"
		exit 0;;
	esac
	shift
done

cryptsetup luksOpen $container_path $volume_name
mkdir -p /mnt/$volume_name
mount /dev/mapper/$volume_name /mnt/$volume_name



echo "volume_name=$volume_name" >/tmp/.lukscryptinfo
echo "Volume has been mounted at /mnt/$volume_name"
