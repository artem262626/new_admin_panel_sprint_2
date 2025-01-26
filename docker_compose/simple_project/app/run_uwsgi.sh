#!/usr/bin/env bash

set -e

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

uwsgi --strict --ini uwsgi.ini
