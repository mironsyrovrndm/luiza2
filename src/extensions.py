from flask import Flask


def init_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""
    # Extension initialization hook.
    _ = app
