#!/bin/bash

# Wait for database if needed (for future use)
# python manage.py wait_for_db

# Apply database migrations
echo "Applying database migrations..."
poetry run python manage.py migrate

# Collect static files
echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
poetry run gunicorn travelTAF.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 3 \
    --timeout 60 \
    --reload \
    --access-logfile - \
    --error-logfile - \
    --log-level debug 