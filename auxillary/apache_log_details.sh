#!/bin/bash
# Menu-driven collection from an apache access.log file
# USAGE:
#       $0 /path/to/access.log
#       $0

if [ -z "$1" ]; then
    read -p "Provide the path to your access.log: " access_log
    if [ ! -f $access_log ]; then
        echo "File not found!"
        exit 1
    fi
else [ ! -f $1 ];
    echo "File not found!";
    exit 2;
fi

echo -e "Connections made:\n"
cat $access_log |cut -d " " -f 1 |sort | uniq -c |sort -urn
echo -e "\nPlease wait, this next part can take a bit...\n"
echo -e "Finding files by access\n"
for ip in $(cat $access_log |cut -d " " -f 1 |sort | uniq -c |sort -urn | awk '{print $2}'); do cat $access_log| grep $ip |cut -d "\"" -f 2 |uniq -c; done |sort -u

# read -p "Provide what you wish to investiage further: " inv_menu;
echo "Provide what you wish to investiagate further: "
options=("Specific Address" "Specific file accessed by specific ip address" "Exit")
select inv_menu in "${options[@]}"; do
     case $inv_menu in
         "Specific Address" ) read -p "Provide the IP address: " inv_address;
             echo -e "Pages accessed by $inv_address by count:\n";
             cat $access_log |grep "$inv_address" | cut -d "\"" -f 2 |uniq -c;; #&
         "Specific file accessed by specific ip address" ) if [ -z "$inv_address" ];
                then
                        echo -e "INFO: No IP address cached\n";
                        read -p "Provide the IP address: " inv_address;
                else
                        read -p "Want to use $inv_address as the IP address? (y/n)" yn
                        case $yn in
                                [Yy]* ) ;;
                                [Nn]* ) read -p "Provide the IP address: " $inv_address;;
                                * ) echo "Please answer yes or no." ;;
                        esac
                fi
                read -p "Provide all or part of the file name you want to see requests for: " http_file;
                echo -e "Unique requests for $inv_address on $http_file\n";
                if [[ $http_file == "" ]]; then
                        echo -e "WARNING! No file name provided!"
                else
                        cat $access_log | grep "$inv_address" | cut -d "\"" -f 2 | uniq -c;
                        echo -e "Number of response codes for $inv_address on $http_file\n";
                        cat $access_log | grep "$inv_address" | grep "$http_file" | sort -u | awk {'print $9'} | uniq -c;
                        read -p "Provide response code to read from, else 'return' " inv_rescode;
                                if [[ $inv_rescode == "return" ]]; then
                                        echo "INFO: Returning"; #&
                                elif [[ $inv_rescode == "Exit" || $inv_rescode == "exit" || $inv_rescode == "Quit" || $inv_rescode == "quit*" ]]; then
                                        exit 0;
                                else
                                        if [[ ! -z "$inv_rescode" ]]; then
                                                echo -e "$inv_rescode requests by $inv_address:\n";
                                                cat $access_log |grep $inv_address |grep $http_file|grep $inv_rescode;
                                        else
                                                echo -e "All requests by $inv_address\n";
                                                cat $access_log |grep $inv_address |grep $http_file;
                                        fi
                                fi
                fi;;
         "Exit" ) echo "Exiting...";
                        exit 0;;
         *) echo "Select from the menu";; #&
     esac
done
