#!/bin/bash
set -e

echo "==> Waiting for PostgreSQL..."
while ! python -c "
import os, psycopg2
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME', 'interngrad'),
    user=os.getenv('DB_USER', 'interngrad_user'),
    password=os.getenv('DB_PASSWORD', ''),
    host=os.getenv('DB_HOST', 'db'),
    port=os.getenv('DB_PORT', '5432'),
)
conn.close()
" 2>/dev/null; do
    echo "    PostgreSQL not ready — retrying in 2s..."
    sleep 2
done
echo "==> PostgreSQL is ready!"

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile -
