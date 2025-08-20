#!/bin/bash

set -o errexit

set -o pipefail

set -o nounset

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Seeding database with dummy users if needed..."
python manage.py seed_users

echo "Running Development Server..."
python manage.py runserver 0.0.0.0:8000
#TODO use gunicorn for prod
# exec gunicorn star_wars.wsgi:application --bind 0.0.0.0:8000 --workers 4
# exec gunicorn api.wsgi:application \
#     --bind 0.0.0.0:8000 \
#     --workers 3 \
#     --threads 2 \
#     --timeout 120