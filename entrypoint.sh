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

    db_settings = connection.settings_dict
    env = os.environ.copy()
    env["PGPASSWORD"] = str(db_settings.get("PASSWORD") or "")
    base_cmd = [
        "psql",
        "-v", "ON_ERROR_STOP=1",
        "-h", str(db_settings.get("HOST") or "db"),
        "-p", str(db_settings.get("PORT") or "5432"),
        "-U", str(db_settings.get("USER") or "postgres"),
        "-d", str(db_settings.get("NAME") or "postgres"),
    ]

    sql_01 = "/app/db/init/01_schema_plus.sql"
    if not roles_table and os.path.exists(sql_01):
        print("==> Tabla 'plus.roles' no encontrada. Cargando /app/db/init/01_schema_plus.sql...")
        subprocess.run(base_cmd + ["-f", sql_01], env=env, check=True)
        print("==> Esquema SQL 01_schema_plus.sql cargado exitosamente.")
    else:
        print("==> Esquema base 'plus' ya inicializado.")

    sql_02 = "/app/db/init/02_ampliaciones_v1_2.sql"
    if os.path.exists(sql_02):
        print("==> Aplicando ampliaciones idempotentes /app/db/init/02_ampliaciones_v1_2.sql (AMP-01 a AMP-12)...")
        subprocess.run(base_cmd + ["-f", sql_02], env=env, check=True)
        print("==> Ampliaciones AMP-01 a AMP-12 aplicadas exitosamente.")

    with connection.cursor() as cursor:
        cursor.execute("SELECT to_regclass('django_migrations');")
        if cursor.fetchone()[0]:
            cursor.execute(
                """
                DELETE FROM django_migrations
                WHERE app IN (
                    'territories', 'accounts', 'audit', 'cases', 'tracking',
                    'communications', 'initiatives', 'news', 'notifications'
                );
                """
            )
PYCODE

echo "==> Aplicando tablas base de Django (contenttypes, auth, admin, authtoken, sessions)..."
python manage.py migrate contenttypes --noinput
python manage.py migrate auth --noinput
python manage.py migrate admin --noinput
python manage.py migrate authtoken --noinput
python manage.py migrate sessions --noinput

echo "==> Sincronizando historial de migraciones de las apps de dominio PLUS (--fake)..."
python manage.py migrate --fake --noinput

echo "==> Inicializando catálogos y roles base de PLUS..."
python manage.py seed_plus_initial

echo "==> Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "==> Iniciando servidor Gunicorn en 0.0.0.0:8000..."
exec "$@"
