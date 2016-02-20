DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SHODAN_API_KEY=$(cat $DIR/SHODAN_API_KEY)
curl -H "Accept: application/json" "https://api.shodan.io/shodan/host/$1?key=$SHODAN_API_KEY" 
