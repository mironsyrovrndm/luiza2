from uuid import uuid4

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from src.db import get_connection

ALLOWED_CATEGORIES = {"hero", "about", "uploads"}


def save_photo(category: str, file: FileStorage) -> str:
    if category not in ALLOWED_CATEGORIES:
        raise ValueError("Unsupported photo category")

    photo_id = uuid4().hex
    filename = secure_filename(file.filename or f"{photo_id}.bin")
    mime_type = file.mimetype or "application/octet-stream"
    payload = file.read()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO photos (id, category, filename, mime_type, payload)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (photo_id, category, filename, mime_type, payload),
            )

    return photo_id


def get_photo(photo_id: str, category: str | None = None) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            if category:
                cur.execute(
                    """
                    SELECT id, category, filename, mime_type, payload
                    FROM photos
                    WHERE id = %s AND category = %s
                    """,
                    (photo_id, category),
                )
            else:
                cur.execute(
                    """
                    SELECT id, category, filename, mime_type, payload
                    FROM photos
                    WHERE id = %s
                    """,
                    (photo_id,),
                )
            row = cur.fetchone()

    if not row:
        return None

    return {
        "id": row[0],
        "category": row[1],
        "filename": row[2],
        "mime_type": row[3],
        "payload": bytes(row[4]),
    }


def list_photo_ids(category: str) -> list[str]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM photos
                WHERE category = %s
                ORDER BY created_at DESC
                """,
                (category,),
            )
            rows = cur.fetchall()
    return [row[0] for row in rows]


def delete_photo(photo_id: str, category: str | None = None) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            if category:
                cur.execute(
                    "DELETE FROM photos WHERE id = %s AND category = %s",
                    (photo_id, category),
                )
            else:
                cur.execute("DELETE FROM photos WHERE id = %s", (photo_id,))
            return cur.rowcount > 0
