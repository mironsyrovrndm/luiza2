import json
from pathlib import Path
from typing import Any

from src.settings import Config

DEFAULT_CONTENT: dict[str, Any] = {
    "hero_label": "Клиент-центрированный психотерапевт",
    "hero_title": "Каждая личность целостна и достаточна",
    "hero_text": "Бережно сопровождаю в поиске опоры, устойчивости и собственного пути — онлайн и очно.",
    "hero_button": "Записаться на консультацию →",
    "hero_image": "",
    "about_title": "Обо мне",
    "about_image": "",
    "about_education": [
        "Московский психолого-социальный университет, 2008–2013",
        "МГППУ, магистратура, 2014–2016",
        "ОППЛ, супервизор, 2021–2023",
    ],
    "products_title": "Продукты",
    "products": [
        {
            "badge": "Бот-тренинг",
            "title": "Зеркало социальных привычек",
            "text": "Интерактивный бот, который поможет увидеть себя в группах по-новому.",
            "meta": "5 дней · Голосовые подкасты",
        },
        {
            "badge": "Тренинг",
            "title": "Сила групп: как быть собой",
            "text": "Практический тренинг для комфортного выстраивания отношений с людьми.",
            "meta": "апрель 2026",
        },
        {
            "badge": "Лекция",
            "title": "Самораскрытие в терапии",
            "text": "Как использовать самораскрытие этично и уместно в терапевтическом процессе.",
            "meta": "Бесплатно · 35 минут",
        },
        {
            "badge": "Обучение",
            "title": "Феномены в консультировании",
            "text": "Изучение феноменов в терапевтическом альянсе вне зависимости от подхода.",
            "meta": "38 000 ₽",
        },
        {
            "badge": "Лекции",
            "title": "Базовые правила терапевтического процесса",
            "text": "Запрос, сеттинг, структура работы — основы для начинающих психологов.",
            "meta": "от 7 000 ₽",
        },
        {
            "badge": "Практикум",
            "title": "Сила блога",
            "text": "Как вести блог легко, аутентично и регулярно. Всегда будут темы.",
            "meta": "5 000 ₽",
        },
    ],
    "clients_title": "Клиентам",
    "clients_subtitle": "Форматы терапии, которые помогут решить ваш запрос.",
    "clients": [
        {
            "title": "Краткосрочная терапия",
            "text": "Подходит для разрешения конкретного запроса точечно и эффективно.",
        },
        {
            "title": "Долгосрочная психотерапия",
            "text": "Глубокая работа, направленная на изменения в структуре личности.",
        },
        {
            "title": "Разовая консультация",
            "text": "Для тех, кто хочет получить вектор для самостоятельной работы.",
        },
    ],
    "supervision_title": "Супервизия",
    "supervision_subtitle": "Поддержка для начинающих и опытных специалистов.",
    "supervision": [
        {
            "title": "Разовая супервизия",
            "price": "6 000 ₽",
            "meta": "40 минут",
            "bullets": [
                "Разбор конкретного случая",
                "Обратная связь",
                "Рекомендации по работе",
            ],
        },
        {
            "title": "Супервизионное сопровождение",
            "price": "25 000 ₽",
            "meta": "5 встреч по 40 минут",
            "bullets": [
                "Встречи раз в неделю",
                "3 месяца поддержки",
                "Личное сопровождение",
            ],
        },
        {
            "title": "Супервизия групп",
            "price": "10 000 ₽",
            "meta": "групповая",
            "bullets": [
                "Анализ групповой динамики",
                "Для групповых терапевтов",
                "Ведение групп любого формата",
            ],
        },
    ],
    "speaker_title": "Я — спикер",
    "speaker_text": "Провожу лекции и воркшопы на темы эмоциональной устойчивости и отношений.",
    "speaker_button": "Сотрудничать",
    "contacts_title": "Контакты",
    "contacts_text": "Оставьте заявку и мы подберем удобное время.",
    "contacts_phone": "+7 (900) 000-00-00",
    "contacts_email": "hello@luiza-psy.ru",
    "contacts_telegram": "@luiza_psy",
}


def _store_path() -> Path:
    return Path(Config.CONTENT_FILE)


def load_content() -> dict[str, Any]:
    path = _store_path()
    if not path.exists():
        return DEFAULT_CONTENT.copy()
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    merged = DEFAULT_CONTENT.copy()
    merged.update(data)
    return merged


def save_content(payload: dict[str, Any]) -> None:
    path = _store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
