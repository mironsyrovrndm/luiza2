#!/bin/sh
set -e

export SQITCH_CONFIG=/app/sqitch/sqitch.conf

if [ -z "${SQITCH_TARGET:-}" ]; then
  echo "ERROR: SQITCH_TARGET is not set"
  exit 1
fi

# извлекаем host/port/user/db из DATABASE_URL (проще) или задай отдельными env
# здесь самый простой путь: используем pg_isready по host db и user из env Postgres
: "${POSTGRES_USER:=psy_user}"
: "${POSTGRES_DB:=psy_db}"
: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"

echo "Waiting for Postgres ${DB_HOST}:${DB_PORT}..."
i=0
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; do
  i=$((i+1))
  if [ "$i" -ge 60 ]; then
    echo "ERROR: Postgres not ready after 60s"
    exit 1
  fi
  sleep 1
done

echo "Running sqitch deploy..."
sqitch deploy "$SQITCH_TARGET"

echo "Starting main process: $*"
exec "$@"
