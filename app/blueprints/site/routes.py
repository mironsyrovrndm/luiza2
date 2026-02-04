from datetime import datetime
from flask import jsonify, redirect, render_template, request, url_for

from app.blueprints.site import site_bp
from app.content_store import load_content
from app.gallery_store import list_gallery_images
from app.records_store import add_record
from app.storage import public_url


def _list_gallery_images() -> list[str]:
    images = list_gallery_images()
    return [
        {
            "id": image.id,
            "filename": image.filename,
            "url": public_url("uploads", image.storage_key),
        }
        for image in images
    ]


@site_bp.get("/")
def index():
    content = load_content()
    content["hero_image_url"] = (
        public_url("hero", content.get("hero_image_key", content.get("hero_image", "")))
        if content.get("hero_image")
        else ""
    )
    content["about_image_url"] = (
        public_url("about", content.get("about_image_key", content.get("about_image", "")))
        if content.get("about_image")
        else ""
    )
    gallery_images = _list_gallery_images()
    submitted = request.args.get("submitted") == "1"
    return render_template(
        "site/index.html",
        content=content,
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


@site_bp.get("/healthz")
def healthcheck():
    return jsonify({"status": "ok"})
