#!/bin/bash
set -e

echo "==> Installing dependencies"
pip install -r requirements.txt

echo "==> Running migrations"
python manage.py migrate --noinput

echo "==> Collecting static"
python manage.py collectstatic --noinput

echo "==> Starting gunicorn"
exec gunicorn animecalendar.wsgi:application --bind 0.0.0.0:${PORT:-8000}
