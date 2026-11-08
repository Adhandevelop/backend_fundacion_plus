#!/bin/sh
set -e

echo "==> Aplicando migraciones de Django en PostgreSQL/PostGIS (--fake-initial para convivir con 01_schema_plus.sql)..."
python manage.py migrate --fake-initial --noinput

echo "==> Inicializando catálogos y roles base de PLUS..."
python manage.py seed_plus_initial

echo "==> Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "==> Iniciando servidor Gunicorn..."
exec "$@"
