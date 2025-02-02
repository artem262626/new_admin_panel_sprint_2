#!/bin/sh
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres at $DB_HOST:$DB_PORT..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.5
    done
    echo "PostgreSQL started"
fi

python manage.py migrate
exec "$@"
