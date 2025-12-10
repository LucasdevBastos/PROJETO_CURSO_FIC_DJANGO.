web: gunicorn animecalendar.wsgi --log-file -
release: python manage.py migrate && python manage.py import_animes --limit 50
