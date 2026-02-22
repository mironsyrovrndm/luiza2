from contextlib import contextmanager
from threading import Lock
from typing import Iterator

import psycopg2
from psycopg2 import OperationalError

from src.settings import DATABASE_URL


class DBUnavailableError(RuntimeError):
    """Raised when no database endpoint is reachable."""


_SCHEMA_BOOTSTRAPPED = False
_SCHEMA_LOCK = Lock()


def _dsn_candidates() -> list[str]:
    candidates = [DATABASE_URL]
    if "@db:" in DATABASE_URL or "@db/" in DATABASE_URL:
        candidates.append(
            DATABASE_URL.replace("@db:", "@host.docker.internal:").replace(
                "@db/", "@host.docker.internal/"
            )
        )
        candidates.append(
            DATABASE_URL.replace("@db:", "@localhost:").replace("@db/", "@localhost/")
        )
    return list(dict.fromkeys(candidates))


def _connect() -> psycopg2.extensions.connection:
    last_error: Exception | None = None
    for dsn in _dsn_candidates():
        try:
            return psycopg2.connect(dsn)
        except OperationalError as exc:
            last_error = exc
            continue

    message = str(last_error) if last_error else "Database is unavailable"
    raise DBUnavailableError(message)


def _ensure_schema(conn: psycopg2.extensions.connection) -> None:
    global _SCHEMA_BOOTSTRAPPED
    if _SCHEMA_BOOTSTRAPPED:
        return

    with _SCHEMA_LOCK:
        if _SCHEMA_BOOTSTRAPPED:
            return
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS site_content (
                    key text PRIMARY KEY,
                    payload jsonb NOT NULL,
                    updated_at timestamptz NOT NULL DEFAULT now()
                );

                CREATE TABLE IF NOT EXISTS records (
                    id text PRIMARY KEY,
                    date text NOT NULL,
                    name text NOT NULL,
                    phone text NOT NULL,
                    telegram text NOT NULL DEFAULT '',
                    complaint text NOT NULL,
                    status text NOT NULL DEFAULT 'Новая',
                    created_at timestamptz NOT NULL DEFAULT now(),
                    updated_at timestamptz NOT NULL DEFAULT now()
                );

                CREATE TABLE IF NOT EXISTS photos (
                    id text PRIMARY KEY,
                    category text NOT NULL CHECK (category IN ('hero', 'about', 'uploads')),
                    filename text NOT NULL,
                    mime_type text NOT NULL,
                    payload bytea NOT NULL,
                    created_at timestamptz NOT NULL DEFAULT now()
                );

                CREATE INDEX IF NOT EXISTS photos_category_created_idx
                ON photos (category, created_at DESC);
                """
            )
        conn.commit()
        _SCHEMA_BOOTSTRAPPED = True


@contextmanager
def get_connection() -> Iterator[psycopg2.extensions.connection]:
    conn = _connect()
    try:
        _ensure_schema(conn)
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
