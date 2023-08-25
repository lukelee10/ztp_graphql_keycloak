# Base image
FROM docker.io/library/python:3.11-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy pyproject toml
COPY pyproject.toml .

# Install Python dependencies
RUN poetry install --no-root --without=dev --no-interaction

# Copy the Django project code
COPY manage.py .
COPY ztp_browser /app/ztp_browser
COPY apps /app/apps
COPY data /app/data

# Collect static files
RUN poetry run python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 80 8000

# Run migrations as part of container initialization
COPY --chown=python:python docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
