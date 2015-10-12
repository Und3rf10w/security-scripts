#!/bin/bash
if [ -z "$1" ]; then
        echo "[*] Automagically enumerate SMB hosts and SMB info from a given network range"
        echo "[*] Dumps the output to hosts/<host ip address>/enum4linux_smb_info"
        echo "[*] Usage    : $0 <scan range>"
exit 1
fi

nbtscan $1 |tee hosts/nbtscan_info

for host in $(nmap -p 139,445 $1 --open |grep report |cut -d " " -f5); do
    enum4linux -v $host |tee hosts/$host/enum4linux_smb_info;
done

exit 0
