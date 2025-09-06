#!/usr/bin/env bash
set -e

# Ждем БД
echo "Waiting for Postgres at ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432} ..."
until python - <<'PYCODE'
import os, socket, time
host = os.environ.get("POSTGRES_HOST","db")
port = int(os.environ.get("POSTGRES_PORT","5432"))
s = socket.socket()
try:
    s.connect((host, port))
    print("DB is reachable")
except Exception as e:
    print("DB not ready:", e)
    raise
finally:
    s.close()
PYCODE
do
  sleep 1
done

# Миграции
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn electronics.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
