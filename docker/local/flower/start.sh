#!/bin/sh
set -e

echo "Starting Flower..."
exec celery -A api.celery \
    --broker=${CELERY_BROKER:-redis://redis:6379/0} \
    flower \
    --port=5555 \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"