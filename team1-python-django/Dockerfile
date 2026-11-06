# ---- Build stage ----
FROM python:3.12-slim AS build

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# ---- Runtime stage ----
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /usr/local/lib/python3.12/site-packages \
    /usr/local/lib/python3.12/site-packages

COPY --from=build /usr/local/bin /usr/local/bin

COPY cloudcart /app/cloudcart

WORKDIR /app/cloudcart

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn cloudcart.wsgi:application --bind 0.0.0.0:8000"]
