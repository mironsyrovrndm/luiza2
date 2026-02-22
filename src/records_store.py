import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from src.db import DBUnavailableError, get_connection
from src.settings import RECORDS_FILE


def _file_path() -> Path:
    return Path(RECORDS_FILE)


def _load_from_file() -> list[dict[str, Any]]:
    path = _file_path()
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def _save_to_file(records: list[dict[str, Any]]) -> None:
    path = _file_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)


def load_records() -> list[dict[str, Any]]:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, date, name, phone, telegram, complaint, status
                    FROM records
                    ORDER BY created_at DESC
                    """
                )
                rows = cur.fetchall()
        return [
            {
                "id": row[0],
                "date": row[1],
                "name": row[2],
                "phone": row[3],
                "telegram": row[4],
                "complaint": row[5],
                "status": row[6],
            }
            for row in rows
        ]
    except DBUnavailableError:
        return _load_from_file()


def add_record(record: dict[str, Any]) -> None:
    record_id = str(record.get("id") or uuid4().hex)
    payload = {
        "id": record_id,
        "date": str(record.get("date", "")),
        "name": str(record.get("name", "")),
        "phone": str(record.get("phone", "")),
        "telegram": str(record.get("telegram", "")),
        "complaint": str(record.get("complaint", "")),
        "status": str(record.get("status", "Новая")),
    }

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO records (id, date, name, phone, telegram, complaint, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        payload["id"],
                        payload["date"],
                        payload["name"],
                        payload["phone"],
                        payload["telegram"],
                        payload["complaint"],
                        payload["status"],
                    ),
                )
    except DBUnavailableError:
        records = _load_from_file()
        records.insert(0, payload)
        _save_to_file(records)


def update_record_status(record_id: str, status: str) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE records SET status = %s, updated_at = now() WHERE id = %s",
                    (status, record_id),
                )
                return cur.rowcount > 0
    except DBUnavailableError:
        records = _load_from_file()
        updated = False
        for record in records:
            if str(record.get("id")) == record_id:
                record["status"] = status
                updated = True
                break
        if updated:
            _save_to_file(records)
        return updated
