from typing import Any
from uuid import uuid4

from sqlalchemy import desc, select

from app.db import session_scope
from app.models import Record


def load_records() -> list[dict[str, Any]]:
    with session_scope() as session:
        rows = session.execute(select(Record).order_by(desc(Record.created_at))).scalars().all()
        return [
            {
                "id": row.id,
                "date": row.date,
                "name": row.name,
                "phone": row.phone,
                "telegram": row.telegram,
                "complaint": row.complaint,
                "status": row.status,
            }
            for row in rows
        ]


def add_record(record: dict[str, Any]) -> None:
    with session_scope() as session:
        record_id = record.get("id") or uuid4().hex
        session.add(
            Record(
                id=record_id,
                date=record["date"],
                name=record["name"],
                phone=record["phone"],
                telegram=record.get("telegram"),
                complaint=record["complaint"],
                status=record.get("status", "Новая"),
            )
        )


def update_record_status(record_id: str, status: str) -> bool:
    with session_scope() as session:
        row = session.get(Record, record_id)
        if not row:
            return False
        row.status = status
        return True
