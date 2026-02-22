import json
from pathlib import Path
from typing import Any

from src import settings

DEFAULT_CONTENT: dict[str, Any] = {
    "main_title": "KATI SHEX",
    "subtitle": "ARTIST / CREATOR",
    "hero_bg": "hero/default.jpg",
    "location": "Moscow",
    "about_title": "Обо мне",
    "about_text": "Короткий текст о вас.",
    "about_stats_title": "Достижения",
    "about_stats": ["10+ лет опыта", "100+ проектов"],
    "about_image": "about/default.jpg",
    "represented_bg": "represented/default.jpg",
    "represented_title": "Представлена в",
    "represented_list": ["Agency 1", "Agency 2"],
    "gallery": [],
}


def _store_path() -> Path:
    return Path(settings.CONTENT_FILE)


def load_content() -> dict[str, Any]:
    path = _store_path()
    if not path.exists():
        return DEFAULT_CONTENT.copy()
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    merged = DEFAULT_CONTENT.copy()
    if isinstance(data, dict):
        merged.update(data)
    return merged


def save_content(payload: dict[str, Any]) -> None:
    path = _store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
