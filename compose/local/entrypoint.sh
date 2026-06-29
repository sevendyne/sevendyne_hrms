#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
while ! python -c "
import socket
import os
url = os.environ.get('DATABASE_URL', '')
host = 'db'
port = 5432
if '@' in url:
    part = url.split('@')[1].split('/')[0]
    if ':' in part:
        host, port = part.split(':')
        port = int(port)
s = socket.socket()
s.settimeout(1)
try:
    s.connect((host, port))
except OSError:
    raise SystemExit(1)
finally:
    s.close()
" 2>/dev/null; do
  sleep 1
done

echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Loading fixtures..."
python manage.py loaddata countries states 2>/dev/null || true

echo "Seeding demo data..."
python manage.py create_groups_and_permissions 2>/dev/null || true
python manage.py seed_demo_data

exec "$@"
