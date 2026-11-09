FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Upgrade available OS packages
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root application user
RUN useradd --create-home --uid 10001 appuser

# Copy Django application
COPY --chown=appuser:appuser cloudcart /app/cloudcart

# Run application as non-root user
USER appuser

WORKDIR /app/cloudcart

EXPOSE 8000

# Run migrations and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn cloudcart.wsgi:application --bind 0.0.0.0:8000"]
