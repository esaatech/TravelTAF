#!/bin/bash

# Collect static files
echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
poetry run python manage.py migrate

# Start Gunicorn with specific bind address
echo "Starting Gunicorn..."
poetry run gunicorn travelTAF.wsgi:application --bind 0.0.0.0:8000 -c gunicorn_config.py --reload 