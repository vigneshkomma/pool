# syntax=docker/dockerfile:1
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_DEBUG=false \
    DJANGO_ALLOWED_HOSTS=poolapp.duckdns.org \
    DJANGO_CSRF_TRUSTED_ORIGINS=https://poolapp.duckdns.org \
    DJANGO_SQLITE_PATH=/app/data/db.sqlite3

WORKDIR /app

# Install dependencies separately so this layer is reused unless they change.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Migrations are safe for a single-container deployment. For multiple replicas,
# run this migration command once as a separate release step instead.
CMD ["/bin/sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && exec gunicorn --bind 0.0.0.0:8000 --workers 3 --access-logfile - --error-logfile - pool.wsgi:application"]
