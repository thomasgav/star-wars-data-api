#!/bin/bash

set -o errexit

set -o pipefail

set -o nounset

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Seeding database with dummy users if needed..."
python manage.py seed_users

if [ "$BUILD_ENV" = "dev" ]; then
    echo "Running Development Server..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "Running Gunicorn..."
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 4 \
        --threads 4 \
        --timeout 120
fi
# exec gunicorn star_wars.wsgi:application --bind 0.0.0.0:8000 --workers 4