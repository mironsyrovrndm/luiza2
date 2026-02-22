from typing import Any
from uuid import uuid4

from src.db import get_connection


def load_records() -> list[dict[str, Any]]:
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


def add_record(record: dict[str, Any]) -> None:
    record_id = str(record.get("id") or uuid4().hex)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO records (id, date, name, phone, telegram, complaint, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    record_id,
                    str(record.get("date", "")),
                    str(record.get("name", "")),
                    str(record.get("phone", "")),
                    str(record.get("telegram", "")),
                    str(record.get("complaint", "")),
                    str(record.get("status", "Новая")),
                ),
            )


def update_record_status(record_id: str, status: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE records SET status = %s, updated_at = now() WHERE id = %s",
                (status, record_id),
            )
            return cur.rowcount > 0
