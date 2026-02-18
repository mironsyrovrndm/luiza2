FROM python:3.12.11-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=linux
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps:
# - supervisor: управляет uwsgi
# - sqitch + postgresql-client + libdbd-pg-perl: миграции и pg_isready
# - build-essential + libpq-dev: на случай сборки бинарных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    sqitch postgresql-client libdbd-pg-perl \
    build-essential libpq-dev \
    ca-certificates curl \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==1.8.3"

WORKDIR /app

# Poetry без venv (как у тебя в деплое)
RUN poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project false

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --only main

COPY . /app

RUN chmod +x /app/deploy/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/app/deploy/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/app/deploy/supervisord.conf"]
