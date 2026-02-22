import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://psy_user:psy_password@db:5432/psy_db",
    )
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        str(Path(__file__).resolve().parent / "blueprints" / "site" / "static" / "uploads"),
    )
    HERO_UPLOAD_FOLDER = os.getenv(
        "HERO_UPLOAD_FOLDER",
        str(Path(__file__).resolve().parent / "blueprints" / "site" / "static" / "hero"),
    )
    ABOUT_UPLOAD_FOLDER = os.getenv(
        "ABOUT_UPLOAD_FOLDER",
        str(Path(__file__).resolve().parent / "blueprints" / "site" / "static" / "about"),
    )
    CONTENT_FILE = os.getenv(
        "CONTENT_FILE",
        str(Path(__file__).resolve().parent / "data" / "content.json"),
    )
    RECORDS_FILE = os.getenv(
        "RECORDS_FILE",
        str(Path(__file__).resolve().parent / "data" / "records.json"),
    )
