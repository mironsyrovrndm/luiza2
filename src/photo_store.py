from pathlib import Path
from uuid import uuid4

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from src.db import get_connection
from src.settings import ABOUT_UPLOAD_FOLDER, HERO_UPLOAD_FOLDER, UPLOAD_FOLDER

ALLOWED_CATEGORIES = {"hero", "about", "uploads"}


def _category_dir(category: str) -> Path:
    if category == "hero":
        return Path(HERO_UPLOAD_FOLDER)
    if category == "about":
        return Path(ABOUT_UPLOAD_FOLDER)
    return Path(UPLOAD_FOLDER)


def _save_local_copy(photo_id: str, category: str, payload: bytes) -> None:
    target_dir = _category_dir(category)
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / photo_id).write_bytes(payload)


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

    _save_local_copy(photo_id, category, payload)
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
    deleted = False
    effective_category = category
    with get_connection() as conn:
        with conn.cursor() as cur:
            if category:
                cur.execute(
                    "DELETE FROM photos WHERE id = %s AND category = %s",
                    (photo_id, category),
                )
            else:
                cur.execute("SELECT category FROM photos WHERE id = %s", (photo_id,))
                row = cur.fetchone()
                if row:
                    effective_category = row[0]
                cur.execute("DELETE FROM photos WHERE id = %s", (photo_id,))
            deleted = cur.rowcount > 0

    if deleted and effective_category:
        local_file = _category_dir(effective_category) / photo_id
        if local_file.exists():
            local_file.unlink()
    return deleted
