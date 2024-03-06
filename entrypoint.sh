#!/bin/bash

# Collect static files
# echo "Collect static files"
# python manage.py collectstatic --noinput
# Start ssh
service ssh start
# Apply database migrations
# echo "Apply database migrations"
# python manage.py makemigrations
# python manage.py migrate

# Start server
echo "Starting server"
gunicorn --bind 0.0.0.0:8000 config.wsgi:application --log-level info \
# python manage.py runserver 0.0.0.0:8000 \
& celery -A config worker -l info
