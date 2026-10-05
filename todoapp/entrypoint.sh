#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

until pg_isready -h db -p 5432 -U todo -d todoapp; do
    sleep 1
done

echo "PostgreSQL is ready."

mkdir -p /static
cp -r /opt/static-dist/. /static/

flask --app wsgi db upgrade

exec "$@"