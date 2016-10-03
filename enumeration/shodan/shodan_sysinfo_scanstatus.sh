DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SHODAN_API_KEY=$(cat $DIR/SHODAN_API_KEY)
curl --silent -X GET -H 'Accept: application/json' "https://api.shodan.io/shodan/scan/$1?key=$SHODAN_API_KEY&id=$1"  | python -mjson.tool
printf '\n'
