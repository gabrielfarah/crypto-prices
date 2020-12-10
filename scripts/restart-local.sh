#!/usr/bin/env bash

service=$1
script_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
docker_compose_path=${script_path}/../deploy/docker-compose.yml

for i in "$@"
do
case $i in
    -s=*|--service=*)
    service="${i#*=}"
    shift # past argument=value
    ;;
    --async)
    service=async
    shift # past argument=value
    ;;
    *)
    	echo "Unknown Option $i"
    ;;
esac
done

if [ "$service" = "async" ] ; then
    docker_compose_path=${script_path}/../deploy/docker-compose-rq.yml
fi

docker-compose -f ${docker_compose_path} restart

echo "== Application Started"
