from importlib import import_module

from flask import Blueprint, Flask

from src.extensions import init_extensions


def create_app(name: str = __name__) -> Flask:
    app = Flask(name, static_folder=None)
    app.config.from_pyfile("settings.py")
    app.config.from_envvar("FLASK_SETTINGS", silent=True)
    register_blueprints(app)
    init_extensions(app)
    return app


def register_blueprints(app: Flask) -> None:
    for name in app.config.get("BLUEPRINTS", []):
        module = import_module(f"src.blueprints.{name}")
        for item_name in dir(module):
            item = getattr(module, item_name)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)


app = create_app()
