import os

DEBUG = os.getenv("DEBUG", "1") in {"1", "true", "True"}

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

DATA_PATH = os.getenv("DATA_PATH", "/data")
UPLOAD_PATH = os.getenv("UPLOAD_PATH", "/uploads")

BLUEPRINTS = ["site", "admin"]

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://psy_user:psy_password@db:5432/psy_db")
CONTENT_FILE = os.getenv("CONTENT_FILE", f"{DATA_PATH}/content.json")
RECORDS_FILE = os.getenv("RECORDS_FILE", f"{DATA_PATH}/records.json")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", f"{UPLOAD_PATH}/uploads")
HERO_UPLOAD_FOLDER = os.getenv("HERO_UPLOAD_FOLDER", f"{UPLOAD_PATH}/hero")
ABOUT_UPLOAD_FOLDER = os.getenv("ABOUT_UPLOAD_FOLDER", f"{UPLOAD_PATH}/about")
