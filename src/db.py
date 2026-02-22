from contextlib import contextmanager
from typing import Iterator

import psycopg2

from src.settings import DATABASE_URL


@contextmanager
def get_connection() -> Iterator[psycopg2.extensions.connection]:
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
