#!/usr/bin/env bash

set -e

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Seeding database with dummy users if needed..."
python manage.py seed_users

echo "Running Development Server..."
python manage.py runserver 0.0.0.0:8000
