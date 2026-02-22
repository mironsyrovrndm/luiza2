from pathlib import Path

from flask import abort, current_app, render_template, send_from_directory

from src.blueprints.landing import landing
from src.content_store import load_content


@landing.get("/")
def index():
    return render_template("landing/index.html", data=load_content())


@landing.get("/uploads/<path:filename>")
def uploads(filename: str):
    upload_root = Path(current_app.config.get("UPLOAD_PATH", "/uploads"))
    file_path = upload_root / filename
    if not file_path.exists() or not file_path.is_file():
        abort(404)
    return send_from_directory(upload_root, filename)
