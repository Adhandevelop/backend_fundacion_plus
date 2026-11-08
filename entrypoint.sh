#!/bin/sh
set -e

echo "==> Verificando esquema 'plus' y tablas en PostgreSQL/PostGIS..."
python - <<'PYCODE'
import os
import subprocess
import django
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

if connection.vendor == "postgresql":
    with connection.cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS plus;")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
        cursor.execute("SELECT to_regclass('plus.roles');")
        roles_table = cursor.fetchone()[0]

    sql_path = "/app/db/init/01_schema_plus.sql"
    if not roles_table and os.path.exists(sql_path):
        print("==> Tabla 'plus.roles' no encontrada. Cargando automáticamente /app/db/init/01_schema_plus.sql en PostgreSQL...")
        db_settings = connection.settings_dict
        env = os.environ.copy()
        env["PGPASSWORD"] = str(db_settings.get("PASSWORD") or "")
        cmd = [
            "psql",
            "-v", "ON_ERROR_STOP=1",
            "-h", str(db_settings.get("HOST") or "db"),
            "-p", str(db_settings.get("PORT") or "5432"),
            "-U", str(db_settings.get("USER") or "postgres"),
            "-d", str(db_settings.get("NAME") or "postgres"),
            "-f", sql_path,
        ]
        subprocess.run(cmd, env=env, check=True)
        print("==> Esquema SQL 01_schema_plus.sql cargado exitosamente.")
    else:
        print("==> Esquema 'plus' ya se encuentra inicializado en PostgreSQL.")
PYCODE

echo "==> Sincronizando historial de migraciones de Django (--fake-initial)..."
python manage.py migrate --fake-initial --noinput

echo "==> Inicializando catálogos y roles base de PLUS..."
python manage.py seed_plus_initial

echo "==> Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "==> Iniciando servidor Gunicorn en 0.0.0.0:8000..."
exec "$@"
