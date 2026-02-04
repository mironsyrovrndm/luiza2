from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.db import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(String(32), primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SiteContent(Base):
    __tablename__ = "site_content"

    id = Column(Integer, primary_key=True)
    data = Column(JSONB, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Record(Base):
    __tablename__ = "records"

    id = Column(String(32), primary_key=True)
    date = Column(String(32), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(100), nullable=False)
    telegram = Column(String(100), nullable=True)
    complaint = Column(Text, nullable=False)
    status = Column(String(50), default="Новая", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class GalleryImage(Base):
    __tablename__ = "gallery_images"

    id = Column(String(32), primary_key=True)
    filename = Column(String(255), nullable=False)
    storage_key = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
