import os
from pathlib import Path

import boto3
from PIL import Image
from werkzeug.utils import secure_filename

from app.config import Config


def _is_allowed_extension(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg", "gif", "webp"}


def validate_image(file_storage) -> None:
    if not file_storage or file_storage.filename == "":
        raise ValueError("Файл не выбран")
    if not _is_allowed_extension(file_storage.filename):
        raise ValueError("Недопустимое расширение файла")
    if file_storage.mimetype not in Config.ALLOWED_IMAGE_TYPES:
        raise ValueError("Недопустимый тип файла")
    file_storage.stream.seek(0)
    try:
        image = Image.open(file_storage.stream)
        image.verify()
    except Exception as exc:
        raise ValueError("Файл не является корректным изображением") from exc
    finally:
        file_storage.stream.seek(0)


def _s3_client():
    return boto3.client("s3", region_name=Config.S3_REGION or None)


def _s3_key(category: str, filename: str) -> str:
    prefix = Config.S3_PREFIX.strip("/")
    return f"{prefix}/{category}/{filename}" if prefix else f"{category}/{filename}"


def _public_s3_url(key: str) -> str:
    if Config.S3_PUBLIC_BASE_URL:
        return f"{Config.S3_PUBLIC_BASE_URL.rstrip('/')}/{key}"
    if Config.S3_REGION:
        return f"https://{Config.S3_BUCKET}.s3.{Config.S3_REGION}.amazonaws.com/{key}"
    return f"https://{Config.S3_BUCKET}.s3.amazonaws.com/{key}"


def use_s3() -> bool:
    return bool(Config.S3_BUCKET)


def save_file(file_storage, directory: str, category: str) -> tuple[str, str]:
    validate_image(file_storage)
    filename = secure_filename(file_storage.filename)
    if use_s3():
        client = _s3_client()
        key = _s3_key(category, filename)
        client.upload_fileobj(
            file_storage.stream,
            Config.S3_BUCKET,
            key,
            ExtraArgs={"ContentType": file_storage.mimetype},
        )
        file_storage.stream.seek(0)
        return filename, key
    upload_dir = Path(directory)
    os.makedirs(upload_dir, exist_ok=True)
    file_storage.save(upload_dir / filename)
    return filename, filename


def delete_file(directory: str, category: str, storage_key: str) -> None:
    if use_s3():
        client = _s3_client()
        client.delete_object(Bucket=Config.S3_BUCKET, Key=storage_key)
        return
    path = Path(directory) / storage_key
    if path.exists():
        path.unlink()


def public_url(category: str, storage_key: str) -> str:
    if use_s3():
        return _public_s3_url(storage_key)
    return f"/static/{category}/{storage_key}"
