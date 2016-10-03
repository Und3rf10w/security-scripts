if [ $# -eq 0 ]
	then
		echo "USAGE: $0 <shodan_api_key>"
		exit 1
fi
curl --silent -H 'Accept: application/json' "https://api.shodan.io/account/profile?key=$1" | python -mjson.tool
printf '\n

