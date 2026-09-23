#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

until pg_isready -d "$DATABASE_URL"; do
    sleep 1
done

echo "PostgreSQL is ready."

flask --app wsgi db upgrade

exec "$@"