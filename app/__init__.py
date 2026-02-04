import logging

from flask import Flask
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException

from app.blueprints.admin import admin_bp
from app.blueprints.site import site_bp
from app.cli import register_cli
from app.config import Config
from app.db import SessionLocal, init_engine


def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=Config.TRUSTED_PROXY_COUNT, x_proto=1)

    init_engine(Config.DATABASE_URL)
    csrf = CSRFProtect()
    csrf.init_app(app)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    app.register_blueprint(site_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    register_cli(app)

    @app.teardown_appcontext
    def remove_session(exception=None):
        SessionLocal.remove()

    @app.errorhandler(403)
    def forbidden(error):
        return "Доступ запрещен", 403

    @app.errorhandler(404)
    def not_found(error):
        return "Страница не найдена", 404

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        return "Некорректный CSRF токен", 400

    @app.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            return error
        app.logger.exception("Unhandled exception: %s", error)
        return "Внутренняя ошибка сервера", 500

    return app
