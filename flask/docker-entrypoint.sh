#!/bin/sh
flask deploy

# enable celery worker in the backgroud
celery worker -A celery_worker.celery -l DEBUG -f /tmp/celery-worker.log &
celery -A celery_worker.celery beat -l INFO --pidfile=/tmp/w1.pid &
celery flower worker -A celery_worker.celery &

# refer to docker best practice:
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# use $@ to get CMD as parameters
exec "$@"
