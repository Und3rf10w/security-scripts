DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SHODAN_API_KEY=$(cat $DIR/SHODAN_API_KEY)
curl -H 'Accept: application/json' "https://api.shodan.io/shodan/scan?key=lT3whkyVHH7iAtP28iNIq7hVNlK638vR" -d "ips=$1"
printf '\n'
