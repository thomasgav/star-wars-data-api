#!/bin/sh
set -e

echo "Starting Celery Beat..."
exec celery -A config beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler #change name
