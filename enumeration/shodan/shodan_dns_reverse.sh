DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SHODAN_API_KEY=$(cat $DIR/SHODAN_API_KEY)
curl --silent -H 'Accept: application/json' "https://api.shodan.io/dns/reverse?key=$SHODAN_API_KEY&ips=$1"  | python -mjson.tool
printf '\n'
