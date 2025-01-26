#!/usr/bin/env bash
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
python manage.py migrate
python manage.py collectstatic --noinput
uwsgi --strict --ini uwsgi.ini
