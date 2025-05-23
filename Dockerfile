# Use specific Python 3.11 version
FROM python:3.11.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
ENV PATH="/opt/poetry/bin:$PATH"
ENV DEBUG=False
ENV PORT=8080
#ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy project files
COPY . .

# Install project
RUN poetry install --no-interaction --no-ansi

# Collect static files
RUN poetry run python manage.py collectstatic --noinput

# Copy the service account key
#COPY service-account-key.json /app/service-account-key.json
#ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

# Expose port
EXPOSE 8080

# Run gunicorn with enhanced logging and configuration
CMD ["poetry", "run", "gunicorn", \
    "travelTAF.wsgi:application", \
    "--bind", "0.0.0.0:8080", \
    "--workers", "2", \
    "--threads", "2", \
    "--timeout", "120", \
    "--log-level", "debug", \
    "--access-logfile", "-", \
    "--error-logfile", "-", \
    "--capture-output"]
    