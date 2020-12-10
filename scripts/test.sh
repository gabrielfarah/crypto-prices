#!/usr/bin/env bash

UNIT=False

for i in "$@"
do
case ${i} in
    -u|--unit)
    UNIT=True
    shift # past argument=value
    ;;
    *)
    	echo "Unknown Option $i"
    ;;
esac
done

script_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
docker_compose_path=${script_path}/../deploy/docker-compose.yml

if [ "$UNIT" = "True" ]; then
	docker-compose -f "${docker_compose_path}" run coins python manage.py test \
	    --no-logs \
		--tag=unit \
		--testrunner=testing.no_db_test_runner.NoDbSetupTestRunner
else
	docker-compose -f "${docker_compose_path}" run coins python manage.py test --failfast
fi

docker-compose -f "${docker_compose_path}" down
