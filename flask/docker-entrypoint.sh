#!/bin/sh
flask db init
flask db migrate
flask db upgrade

# refer to docker best practice:
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# use $@ to get CMD as parameters
exec "$@"
