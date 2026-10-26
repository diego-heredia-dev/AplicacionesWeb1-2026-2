#!/bin/sh

set -e

echo "Esperando a PostgreSQL..."

until pg_isready -h db -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
    sleep 2
done

echo "PostgreSQL está disponible."

echo "Iniciando aplicación Flask..."
exec "$@"