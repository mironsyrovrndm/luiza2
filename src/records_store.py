import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from src import settings


def _store_path() -> Path:
    return Path(settings.RECORDS_FILE)


def load_records() -> list[dict[str, Any]]:
    path = _store_path()
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, list):
        records = [item for item in data if isinstance(item, dict)]
        updated = False
        for record in records:
            if not record.get("id"):
                record["id"] = uuid4().hex
                updated = True
        if updated:
            save_records(records)
        return records
    return []


def save_records(records: list[dict[str, Any]]) -> None:
    path = _store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)


def add_record(record: dict[str, Any]) -> None:
    records = load_records()
    if not record.get("id"):
        record["id"] = uuid4().hex
    records.insert(0, record)
    save_records(records)


def update_record_status(record_id: str, status: str) -> bool:
    records = load_records()
    updated = False
    for record in records:
        if str(record.get("id")) == record_id:
            record["status"] = status
            updated = True
            break
    if updated:
        save_records(records)
    return updated
