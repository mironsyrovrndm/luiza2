import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

from flask import redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from app.blueprints.admin import admin_bp
from app.config import Config
from app.content_store import DEFAULT_CONTENT, load_content, save_content
from app.records_store import add_record, load_records, update_record_status

ALLOWED_EXTENSIONS: set[str] = {"png", "jpg", "jpeg", "gif", "webp"}


def _is_allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _list_uploads() -> Iterable[str]:
    upload_dir = Path(Config.UPLOAD_FOLDER)
    if not upload_dir.exists():
        return []
    return sorted(
        [
            file.name
            for file in upload_dir.iterdir()
            if file.is_file() and _is_allowed(file.name)
        ]
    )


def _split_lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def _parse_products() -> list[dict[str, str]]:
    badges = request.form.getlist("products_badge")
    titles = request.form.getlist("products_title_item")
    texts = request.form.getlist("products_text")
    metas = request.form.getlist("products_meta")
    items = []
    for badge, title, text, meta in zip(badges, titles, texts, metas):
        if any([badge.strip(), title.strip(), text.strip(), meta.strip()]):
            items.append({"badge": badge.strip(), "title": title.strip(), "text": text.strip(), "meta": meta.strip()})
    return items


def _parse_clients() -> list[dict[str, str]]:
    titles = request.form.getlist("clients_title_item")
    texts = request.form.getlist("clients_text")
    items = []
    for title, text in zip(titles, texts):
        if title.strip() or text.strip():
            items.append({"title": title.strip(), "text": text.strip()})
    return items


def _parse_supervision() -> list[dict[str, object]]:
    titles = request.form.getlist("supervision_title_item")
    prices = request.form.getlist("supervision_price")
    metas = request.form.getlist("supervision_meta")
    bullets_raw_list = request.form.getlist("supervision_bullets")
    items = []
    for title, price, meta, bullets_raw in zip(titles, prices, metas, bullets_raw_list):
        bullets = _split_lines(bullets_raw)
        if any([title.strip(), price.strip(), meta.strip(), bullets]):
            items.append(
                {
                    "title": title.strip(),
                    "price": price.strip(),
                    "meta": meta.strip(),
                    "bullets": bullets,
                }
            )
    return items


def _save_file(file, upload_dir: Path) -> str:
    filename = secure_filename(file.filename)
    os.makedirs(upload_dir, exist_ok=True)
    file.save(upload_dir / filename)
    return filename


def _format_datetime(date_value: str, time_value: str) -> str:
    if date_value:
        try:
            date_obj = datetime.fromisoformat(date_value)
        except ValueError:
            date_obj = datetime.now()
    else:
        date_obj = datetime.now()

    if time_value:
        try:
            time_obj = datetime.strptime(time_value, "%H:%M")
        except ValueError:
            time_obj = datetime.now()
        combined = datetime.combine(date_obj.date(), time_obj.time())
        return combined.strftime("%d.%m.%Y %H:%M")

    return date_obj.strftime("%d.%m.%Y")


def _parse_record_datetime(value: str) -> datetime | None:
    for fmt in ("%d.%m.%Y %H:%M", "%d.%m.%Y"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


@admin_bp.before_app_request
def require_admin():
    if not request.path.startswith("/admin"):
        return None
    if request.endpoint in {"admin.login", "admin.login_post", "admin.static"}:
        return None
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))
    return None


@admin_bp.get("/login")
def login():
    return render_template("admin/login.html")


@admin_bp.post("/login")
def login_post():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if username == "admin" and password == "admin":
        session["admin_logged_in"] = True
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/login.html", error="Неверный логин или пароль")


@admin_bp.get("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.login"))


@admin_bp.get("/")
def dashboard():
    records = load_records()
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    recent_records = []
    upcoming_records = []
    for record in records:
        date_value = str(record.get("date", ""))
        parsed = _parse_record_datetime(date_value)
        if parsed and parsed >= week_ago:
            recent_records.append(record)
        status = record.get("status", "Новая")
        if status != "Завершен":
            upcoming_records.append(record)

    upcoming_records_sorted = sorted(
        enumerate(upcoming_records),
        key=lambda pair: (
            _parse_record_datetime(str(pair[1].get("date", ""))) or datetime.max,
            pair[0],
        ),
    )
    upcoming_preview = [
        {
            "name": record.get("name", "Без имени"),
            "date": record.get("date", "—"),
            "status": record.get("status", "Новая"),
        }
        for _, record in upcoming_records_sorted[:3]
    ]

    stats = {
        "total": len(records),
        "week_total": len(recent_records),
        "upcoming_total": len(upcoming_records),
    }
    return render_template("admin/dashboard.html", stats=stats, upcoming=upcoming_preview)


@admin_bp.get("/content")
def content():
    uploads = _list_uploads()
    content_data = load_content()
    return render_template("admin/content.html", uploads=uploads, content=content_data)


@admin_bp.post("/content/save", endpoint="save_content")
def save_content_route():
    content_data = load_content()
    payload = {
        **DEFAULT_CONTENT,
        **content_data,
        "hero_label": request.form.get("hero_label", content_data.get("hero_label", "")),
        "hero_title": request.form.get("hero_title", content_data.get("hero_title", "")),
        "hero_text": request.form.get("hero_text", content_data.get("hero_text", "")),
        "hero_button": request.form.get("hero_button", content_data.get("hero_button", "")),
        "about_title": request.form.get("about_title", content_data.get("about_title", "")),
        "about_image": content_data.get("about_image", ""),
        "about_education": _split_lines(request.form.get("about_education", ""))
        or content_data.get("about_education", []),
        "products_title": request.form.get("products_title", content_data.get("products_title", "")),
        "products": _parse_products() or content_data.get("products", []),
        "clients_title": request.form.get("clients_title", content_data.get("clients_title", "")),
        "clients_subtitle": request.form.get("clients_subtitle", content_data.get("clients_subtitle", "")),
        "clients": _parse_clients() or content_data.get("clients", []),
        "supervision_title": request.form.get(
            "supervision_title", content_data.get("supervision_title", "")
        ),
        "supervision_subtitle": request.form.get(
            "supervision_subtitle", content_data.get("supervision_subtitle", "")
        ),
        "supervision": _parse_supervision() or content_data.get("supervision", []),
        "speaker_title": request.form.get("speaker_title", content_data.get("speaker_title", "")),
        "speaker_text": request.form.get("speaker_text", content_data.get("speaker_text", "")),
        "speaker_button": request.form.get("speaker_button", content_data.get("speaker_button", "")),
        "contacts_title": request.form.get("contacts_title", content_data.get("contacts_title", "")),
        "contacts_text": request.form.get("contacts_text", content_data.get("contacts_text", "")),
        "contacts_phone": request.form.get("contacts_phone", content_data.get("contacts_phone", "")),
        "contacts_email": request.form.get("contacts_email", content_data.get("contacts_email", "")),
        "contacts_telegram": request.form.get(
            "contacts_telegram", content_data.get("contacts_telegram", "")
        ),
    }
    save_content(payload)
    return redirect(url_for("admin.content"))


@admin_bp.post("/content/upload-hero")
def upload_hero():
    file = request.files.get("photo")
    if not file or file.filename == "":
        return redirect(url_for("admin.content"))
    if not _is_allowed(file.filename):
        return redirect(url_for("admin.content"))

    filename = _save_file(file, Path(Config.HERO_UPLOAD_FOLDER))
    content_data = load_content()
    content_data["hero_image"] = filename
    save_content(content_data)
    return redirect(url_for("admin.content"))


@admin_bp.post("/content/delete-hero")
def delete_hero():
    content_data = load_content()
    filename = content_data.get("hero_image")
    if filename:
        path = Path(Config.HERO_UPLOAD_FOLDER) / filename
        if path.exists():
            path.unlink()
        content_data["hero_image"] = ""
        save_content(content_data)
    return redirect(url_for("admin.content"))


@admin_bp.post("/content/upload-about")
def upload_about():
    file = request.files.get("photo")
    if not file or file.filename == "":
        return redirect(url_for("admin.content"))
    if not _is_allowed(file.filename):
        return redirect(url_for("admin.content"))

    filename = _save_file(file, Path(Config.ABOUT_UPLOAD_FOLDER))
    content_data = load_content()
    content_data["about_image"] = filename
    save_content(content_data)
    return redirect(url_for("admin.content"))


@admin_bp.post("/content/delete-about")
def delete_about():
    content_data = load_content()
    filename = content_data.get("about_image")
    if filename:
        path = Path(Config.ABOUT_UPLOAD_FOLDER) / filename
        if path.exists():
            path.unlink()
        content_data["about_image"] = ""
        save_content(content_data)
    return redirect(url_for("admin.content"))


@admin_bp.post("/content/upload-gallery")
def upload_gallery():
    files = request.files.getlist("photo")
    if not files:
        return redirect(url_for("admin.content"))

    upload_dir = Path(Config.UPLOAD_FOLDER)
    for file in files:
        if not file or file.filename == "":
            continue
        if not _is_allowed(file.filename):
            continue
        _save_file(file, upload_dir)
    return redirect(url_for("admin.content"))


@admin_bp.post("/content/delete-gallery")
def delete_gallery():
    filename = request.form.get("filename", "")
    if filename:
        path = Path(Config.UPLOAD_FOLDER) / filename
        if path.exists():
            path.unlink()
    return redirect(url_for("admin.content"))


@admin_bp.get("/clients")
def clients():
    created = request.args.get("created") == "1"
    return render_template("admin/clients.html", created=created, records=load_records())


@admin_bp.post("/clients/add", endpoint="add_client")
def add_client():
    date_value = request.form.get("client_date", "").strip()
    time_value = request.form.get("client_time", "").strip()
    name = request.form.get("client_name", "").strip()
    phone = request.form.get("client_phone", "").strip()
    telegram = request.form.get("client_telegram", "").strip()
    complaint = request.form.get("client_complaint", "").strip()
    if name and phone and complaint:
        add_record(
            {
                "date": _format_datetime(date_value, time_value),
                "name": name,
                "phone": phone,
                "telegram": telegram,
                "complaint": complaint,
                "status": "Новая",
            }
        )
    return redirect(url_for("admin.clients", created=1))


@admin_bp.post("/clients/status", endpoint="update_client_status")
def update_client_status_route():
    record_id = request.form.get("record_id", "").strip()
    status = request.form.get("status", "").strip()
    if record_id and status:
        update_record_status(record_id, status)
    return redirect(url_for("admin.clients"))
