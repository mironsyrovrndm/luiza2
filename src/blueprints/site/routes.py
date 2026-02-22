from datetime import datetime
from pathlib import Path

from flask import redirect, render_template, request, url_for

from src.blueprints.site import site_bp
from src.settings import Config
from src.content_store import load_content
from src.records_store import add_record


def _list_gallery_images() -> list[str]:
    upload_dir = Path(Config.UPLOAD_FOLDER)
    if not upload_dir.exists():
        return []
    return sorted([file.name for file in upload_dir.iterdir() if file.is_file()])


@site_bp.get("/")
def index():
    content = load_content()
    data = content
    gallery_images = _list_gallery_images()
    submitted = request.args.get("submitted") == "1"
    return render_template(
        "site/index.html",
        content=content,
        data=data,
        gallery_images=gallery_images,
        submitted=submitted,
    )


@site_bp.post("/contact")
def contact():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    telegram = request.form.get("telegram", "").strip()
    complaint = request.form.get("complaint", "").strip()
    if name and phone and complaint:
        add_record(
            {
                "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "name": name,
                "phone": phone,
                "telegram": telegram,
                "complaint": complaint,
                "status": "Новая",
            }
        )
    return redirect(url_for("site.index", submitted=1))
