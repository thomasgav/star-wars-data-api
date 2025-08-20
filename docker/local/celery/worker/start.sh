#!/bin/bash

set -e

echo "Starting Celery Worker..."
exec celery -A api.celery worker --loglevel=INFO --concurrency=4 -E
