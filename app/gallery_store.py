from uuid import uuid4

from sqlalchemy import desc, select

from app.db import session_scope
from app.models import GalleryImage


def list_gallery_images() -> list[GalleryImage]:
    with session_scope() as session:
        return session.execute(select(GalleryImage).order_by(desc(GalleryImage.created_at))).scalars().all()


def add_gallery_image(filename: str, storage_key: str) -> None:
    with session_scope() as session:
        session.add(GalleryImage(id=uuid4().hex, filename=filename, storage_key=storage_key))


def delete_gallery_image(image_id: str) -> GalleryImage | None:
    with session_scope() as session:
        row = session.get(GalleryImage, image_id)
        if not row:
            return None
        session.delete(row)
        return row
