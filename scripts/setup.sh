#!/usr/bin/env bash

script_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
docker_compose_path=${script_path}/../deploy/docker-compose.yml
SKIP_DB=False


for i in "$@"
do
case $i in
    --skipdb)
    SKIP_DB=True
    shift # past argument=value
    ;;
    *)
    	echo "Unknown Option $i"
    ;;
esac
done

# Running the local docker compose will build all images. Including
# Postgres container with the env variables, which will create the DB
echo "======================"
echo "=== Create local network for all local services"
echo "======================"
docker network create -d bridge pimes_network
# windows doesnt mount properly with virtualbox but creating a volume seperately works
docker volume create --name pimes-postgresql -d local
echo "======================"
echo "=== Building local env"
echo "======================"
if [ "$SKIP_DB" == "False" ]; then
    docker-compose -f ${docker_compose_path} up -d
    echo "======================"
    echo "=== Waiting for build "
    echo "=== Ctrl-C to skip    "
    echo "======================"
fi

echo "======================"
echo "=== Making DB Migrations"
echo "======================"
source "$script_path/make_migrations.sh"
echo

echo "======================"
echo "=== Migrating DB"
echo "======================"
source "$script_path/migratedb.sh"
echo

echo "======================"
echo "=== Creating superuser"
echo "======================"
source "$script_path/createsu.sh"
echo

echo "======================"
echo "=== Collecting assets "
echo "======================"
source "$script_path/collectstatic.sh"
echo

echo "======================"
echo "=== Stopping local env"
echo "======================"
source "$script_path/kill-local.sh"

echo "======================"
echo "=== Running local env"
echo "======================"
source "$script_path/run-local.sh"