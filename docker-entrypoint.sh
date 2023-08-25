#!/bin/sh
set -e

# Check production settings
if [ "$DJANGO_SETTINGS_MODULE" = "ztp_browser.settings.production" ]; then
    poetry run python manage.py check --deploy --fail-level WARNING
fi

# Run migrations
poetry run python manage.py migrate

# FIXME: load this outside of container startup
# Load sample data
poetry run python manage.py loaddata data/sample_data.json

# Start the application server
if [ "$DJANGO_SETTINGS_MODULE" = "ztp_browser.settings.production" ]; then
    exec poetry run gunicorn --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker ztp_browser.asgi:application
else
    exec poetry run python manage.py runserver 0.0.0.0:8000
fi
