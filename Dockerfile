# Python slim, быстрее и легче
FROM python:3.11-slim

# Системные пакеты для psycopg2 и т.п.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
 && rm -rf /var/lib/apt/lists/*

# Оптимизации для pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Зависимости отдельно — лучше кеш
COPY requirements.txt .
RUN pip install -r requirements.txt

# Код
COPY . .

# Статика админки на проде через WhiteNoise
ENV DJANGO_SETTINGS_MODULE=electronics.settings
RUN python manage.py collectstatic --noinput || true

# Скрипт старта
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
