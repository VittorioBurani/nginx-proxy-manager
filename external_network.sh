#!/bin/bash
if [[ $EUID -ne 0 && -z $(groups | grep -o docker) ]]; then
    echo "You must be root or in the docker group to run this script. Exiting..."
    exit 1
fi

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd "$SCRIPTPATH"

if [ -z "$1" ]; then
    echo "Missing command. Usage: $0 <enable|disable> <network_name>"
    exit 1
elif [ "$1" != "enable" ] && [ "$1" != "disable" ]; then
    echo "Wrong command. Usage: $0 <enable|disable> <network_name>"
    exit 1
elif [ -z "$2" ]; then
    echo "Missing network name. Usage: $0 <enable|disable> <network_name>"
    exit 1
elif [ "$1" == "enable" ]; then
    docker compose down
    docker network create $2
    sed -Ei docker-compose.yml \
        -e "s@(#\s)?(networks:)@\2@g" \
        -e "s@(#\s)?(\s+default:)@\2@g" \
        -e "s@(#\s)?(\s+external:) (true|false)@\2 true@g" \
        -e "s@(#\s)?(\s+name:) \S+@\2 $2@g"

elif [ "$1" == "disable" ]; then
    docker compose down
    sed -Ei docker-compose.yml \
        -e "s@(#\s)?(networks:)@# \2@g" \
        -e "s@(#\s)?(\s+default:)@# \2@g" \
        -e "s@(#\s)?(\s+external:) (true|false)@# \2 false@g" \
        -e "s@(#\s)?(\s+name: \S+)@# \2@g"
fi

docker compose up -d
