#!/bin/sh
set -e

# Указываем, где лежит конфиг Sqitch (у тебя он в /app/sqitch/)
export SQITCH_CONFIG=/app/sqitch/sqitch.conf

if [ -z "${SQITCH_TARGET:-}" ]; then
  echo "ERROR: SQITCH_TARGET is not set"
  exit 1
fi

: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"
: "${POSTGRES_USER:=psy_user}"
: "${POSTGRES_DB:=psy_db}"

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
