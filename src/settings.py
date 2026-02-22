import os
from pathlib import Path

DEBUG = os.getenv("DEBUG", "0") in {"1", "true", "True"}

# === Security ===
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

# == Directories ===
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = os.getenv("DATA_PATH", str(BASE_DIR / "data"))
UPLOAD_PATH = os.getenv("UPLOAD_PATH", str(BASE_DIR / "blueprints" / "site" / "static"))

# Blueprints loaded by app factory
BLUEPRINTS = ["site", "admin"]

# Runtime paths used across handlers/stores
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://psy_user:psy_password@db:5432/psy_db")
CONTENT_FILE = os.getenv("CONTENT_FILE", str(Path(DATA_PATH) / "content.json"))
RECORDS_FILE = os.getenv("RECORDS_FILE", str(Path(DATA_PATH) / "records.json"))
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(Path(UPLOAD_PATH) / "uploads"))
HERO_UPLOAD_FOLDER = os.getenv("HERO_UPLOAD_FOLDER", str(Path(UPLOAD_PATH) / "hero"))
ABOUT_UPLOAD_FOLDER = os.getenv("ABOUT_UPLOAD_FOLDER", str(Path(UPLOAD_PATH) / "about"))


class Config:
    SECRET_KEY = SECRET_KEY
    DATABASE_URL = DATABASE_URL
    UPLOAD_FOLDER = UPLOAD_FOLDER
    HERO_UPLOAD_FOLDER = HERO_UPLOAD_FOLDER
    ABOUT_UPLOAD_FOLDER = ABOUT_UPLOAD_FOLDER
    CONTENT_FILE = CONTENT_FILE
    RECORDS_FILE = RECORDS_FILE
