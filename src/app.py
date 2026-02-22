from flask import Flask

from src.blueprints.admin import admin_bp
from src.blueprints.site import site_bp
from src.settings import Config


def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)

    app.register_blueprint(site_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
