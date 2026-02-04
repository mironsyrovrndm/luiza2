import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://psy_user:psy_password@db:5432/psy_db")
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
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(5 * 1024 * 1024)))
    ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "true").lower() == "true"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    ADMIN_ALLOWED_IPS = [
        ip.strip() for ip in os.getenv("ADMIN_ALLOWED_IPS", "").split(",") if ip.strip()
    ]
    TRUSTED_PROXY_COUNT = int(os.getenv("TRUSTED_PROXY_COUNT", "0"))
    S3_BUCKET = os.getenv("S3_BUCKET", "")
    S3_REGION = os.getenv("S3_REGION", "")
    S3_PREFIX = os.getenv("S3_PREFIX", "media")
    S3_PUBLIC_BASE_URL = os.getenv("S3_PUBLIC_BASE_URL", "")
