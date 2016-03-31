if [ $# -eq 0 ]
	then
		echo "USAGE: $0 <shodan_api_key>"
		exit 1
fi
curl --silent -H 'Accept: application/json' "https://api.shodan.io/api-info?key=$1"
printf '\n'
