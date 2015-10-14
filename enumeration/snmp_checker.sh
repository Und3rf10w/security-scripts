#!/bin/bash
if [ -z "$1" ]; then
        echo "[*] Automagically enumerates a given network range for hosts and tries a given set of community strings"
        echo "[*] Dumps the output to hosts/<host ip address>/snmp_check_info"
        echo "[*] Usage    : $0 <scan range> [/path/to/file/with/snmp/strings]"
exit 1
fi

onesixtyone -c $community_file -i $scan_range_file | grep 192. |cut -d " " -f 1| tee snmp_hosts
# snmpcheck -c public -t 192.168.15.203
for string in $(cat community_file); do
	for host in $(cat snmp_hosts); do
		snmpcheck -c $string -t $host |tee hosts/$host/snmp_check_info;
	done
done
