#!/bin/bash
if [ -z "$1" ]; then
	echo "[*] Nmap script to ping a subnet, then fully scan it"
	echo "[*] Dumps the output in XML in hosts/nmap.xml"
	echo "[*] Usage    : $0 <scan range> [comma-separated list of DNS server(s)]"
fi

if [ ! -d "hosts" ]; then
	mkdir hosts;
fi

nmap -sn $1 |grep report |cut -d " " -f 5 |tee ping_sweep

for host in `cat ping_sweep`; do
	if [ ! -d "hosts/$host" ]; then
		mkdir hosts/$host;
	fi
done

if [ -z "$2" ]; then
	nmap -sS -R -A -iL ping_sweep -T5 -e tap0 -oX hosts/nmap.xml -v;
else
	nmap -sS -R --dns-servers $2 -A -iL ping_sweep -T5 -e tap0 -oX hosts/nmap.xml -v;

fi
