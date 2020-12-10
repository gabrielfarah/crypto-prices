#!/usr/bin/env bash

script_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
docker_compose_path=${script_path}/../deploy/docker-compose.yml
docker-compose -f ${docker_compose_path} run coins python manage.py collectstatic --noinput
