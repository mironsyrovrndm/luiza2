FROM python:3.11-slim

ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl build-essential libpq-dev \
        supervisor \
        sqitch libdbd-pg-perl postgresql-client \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root

COPY . /app

RUN chmod +x /app/deploy/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/app/deploy/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/app/deploy/supervisord.conf"]
