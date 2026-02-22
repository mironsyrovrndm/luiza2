from datetime import datetime
from flask import Response, abort, redirect, render_template, request, url_for

from src.blueprints.site import site_bp
from src.content_store import load_content
from src.records_store import add_record
from src.photo_store import get_photo, list_photo_ids


def _list_gallery_images() -> list[str]:
    return list_photo_ids("uploads")


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


@site_bp.get("/media/<category>/<photo_id>")
def media(category: str, photo_id: str):
    photo = get_photo(photo_id, category=category)
    if not photo:
        abort(404)
    return Response(photo["payload"], mimetype=photo["mime_type"])
