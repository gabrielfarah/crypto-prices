#!/bin/sh
# https://github.com/docker-library/postgres/issues/296
python manage.py collectstatic --noinput
python manage.py migrate --noinput
#exec "$@"