#!/bin/sh

if [ "$1" = 'unittest' ]; then
    echo "Waiting for postgres..."

    while ! nc -z db 5432; do
      sleep 0.1
    done
    echo "PostgreSQL started"

    python manage.py test --noinput

else
    echo "Waiting for postgres..."

    while ! nc -z db 5432; do
      sleep 0.1
    done
    echo "PostgreSQL started"

    echo "Migrate the Database at startup of project"
    python manage.py migrate --settings ${DJANGO_SETTINGS_MODULE} --noinput

    echo "Update translation fields"
    python manage.py update_translation_fields --settings ${DJANGO_SETTINGS_MODULE}

    echo "Create admin user"
    python manage.py createsuperuser --email=admin@admin.com --noinput

    echo "RUNNING DEV SERVER DJANGO__________"
    python manage.py runserver 0.0.0.0:8000

    echo "Running gunicorn======================"
    gunicorn finmanager.wsgi:application --bind 0.0.0.0:8000 --config='/app/finmanager/gunicorn.py' --workers=3
fi
