if [ -z $1 ]; then
	echo "[*] DNS Zonetransfer script"
	echo "USAGE    : $0 megacorpone.com"
	exit 1
fi

for server in `host -t ns $1 |cut -d " " -f4`; do
	host -l $1 $server |grep "has address"
done
