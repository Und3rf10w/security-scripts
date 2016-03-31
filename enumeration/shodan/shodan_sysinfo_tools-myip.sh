DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SHODAN_API_KEY=$(cat $DIR/SHODAN_API_KEY)
curl -H 'Accept: application/json' "https://api.shodan.io/tools/myip?key=$SHODAN_API_KEY"  | python -mjson.tool
printf '\n'
