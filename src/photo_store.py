import mimetypes
from pathlib import Path
from uuid import uuid4

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from src.db import DBUnavailableError, get_connection
from src.settings import ABOUT_UPLOAD_FOLDER, HERO_UPLOAD_FOLDER, UPLOAD_FOLDER

ALLOWED_CATEGORIES = {"hero", "about", "uploads"}


def _category_dir(category: str) -> Path:
    if category == "hero":
        return Path(HERO_UPLOAD_FOLDER)
    if category == "about":
        return Path(ABOUT_UPLOAD_FOLDER)
    return Path(UPLOAD_FOLDER)


def _local_photo_path(category: str, photo_id: str, filename: str | None = None) -> Path:
    target_dir = _category_dir(category)
    target_dir.mkdir(parents=True, exist_ok=True)
    if filename:
        suffix = Path(filename).suffix
        if suffix:
            return target_dir / f"{photo_id}{suffix}"
    return target_dir / photo_id


def _find_local_photo(category: str, photo_id: str) -> Path | None:
    target_dir = _category_dir(category)
    exact = target_dir / photo_id
    if exact.exists() and exact.is_file():
        return exact
    matches = sorted(target_dir.glob(f"{photo_id}.*"))
    for match in matches:
        if match.is_file():
            return match
    return None


def _save_local_copy(photo_id: str, category: str, payload: bytes, filename: str) -> None:
    target = _local_photo_path(category, photo_id, filename)
    target.write_bytes(payload)


def save_photo(category: str, file: FileStorage) -> str:
    if category not in ALLOWED_CATEGORIES:
        raise ValueError("Unsupported photo category")

    photo_id = uuid4().hex
    filename = secure_filename(file.filename or f"{photo_id}.bin")
    mime_type = file.mimetype or "application/octet-stream"
    payload = file.read()

    _save_local_copy(photo_id, category, payload, filename)

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO photos (id, category, filename, mime_type, payload)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (photo_id, category, filename, mime_type, payload),
                )
    except DBUnavailableError:
        pass

    return photo_id


def get_photo(photo_id: str, category: str | None = None) -> dict | None:
    if category:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, category, filename, mime_type, payload
                        FROM photos
                        WHERE id = %s AND category = %s
                        """,
                        (photo_id, category),
                    )
                    row = cur.fetchone()
            if row:
                return {
                    "id": row[0],
                    "category": row[1],
                    "filename": row[2],
                    "mime_type": row[3],
                    "payload": bytes(row[4]),
                }
        except DBUnavailableError:
            pass

        local = _find_local_photo(category, photo_id)
        if not local:
            return None
        mime_type = mimetypes.guess_type(local.name)[0] or "application/octet-stream"
        return {
            "id": photo_id,
            "category": category,
            "filename": local.name,
            "mime_type": mime_type,
            "payload": local.read_bytes(),
        }

    # category-agnostic fallback (used rarely)
    for candidate in ALLOWED_CATEGORIES:
        photo = get_photo(photo_id, category=candidate)
        if photo:
            return photo
    return None


def list_photo_ids(category: str) -> list[str]:
    try:
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
    except DBUnavailableError:
        target_dir = _category_dir(category)
        if not target_dir.exists():
            return []
        ids = []
        for file in target_dir.iterdir():
            if not file.is_file() or file.name.startswith('.'):
                continue
            ids.append(file.stem)
        return sorted(ids, reverse=True)


def delete_photo(photo_id: str, category: str | None = None) -> bool:
    deleted = False
    effective_category = category

    try:
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
    except DBUnavailableError:
        deleted = True

    categories = [effective_category] if effective_category else list(ALLOWED_CATEGORIES)
    for cat in categories:
        if not cat:
            continue
        local = _find_local_photo(cat, photo_id)
        if local and local.exists():
            local.unlink()
            deleted = True
    return deleted
