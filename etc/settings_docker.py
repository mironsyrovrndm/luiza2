import os

from src.settings import Config


class DockerConfig(Config):
    """Docker-oriented settings override."""

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://psy_user:psy_password@db:5432/psy_db",
    )
