import os

DEBUG = False

# === Security ===
SECRET_KEY = os.getenv("SECRET_KEY", "!A6s&M0Q'^:)v<;h^MK2)'V#yq*lncN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

# == Directories ===
DATA_PATH = os.getenv("DATA_PATH", "/data")
UPLOAD_PATH = os.getenv("UPLOAD_PATH", "/uploads")

BLUEPRINTS = ["admin", "landing"]

# Backward-compatible keys used by handlers/stores
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://psy_user:psy_password@db:5432/psy_db")
CONTENT_FILE = os.path.join(DATA_PATH, "content.json")
RECORDS_FILE = os.path.join(DATA_PATH, "records.json")
HERO_UPLOAD_FOLDER = os.path.join(UPLOAD_PATH, "hero")
ABOUT_UPLOAD_FOLDER = os.path.join(UPLOAD_PATH, "about")
UPLOAD_FOLDER = os.path.join(UPLOAD_PATH, "gallery")
