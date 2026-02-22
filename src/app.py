from importlib import import_module

from flask import Blueprint, Flask

from src.extensions import init_extensions


def create_app(name: str = __name__) -> Flask:
    _app = Flask(name, static_folder="static", static_url_path="/static")
    _app.config.from_pyfile("settings.py")
    _app.config.from_envvar("FLASK_SETTINGS", silent=True)
    return _app


def register_blueprints(_app: Flask) -> None:
    for name in _app.config.get("BLUEPRINTS", []):
        module = import_module(f"src.blueprints.{name}")

        for item_name in dir(module):
            item = getattr(module, item_name)
            if isinstance(item, Blueprint):
                _app.register_blueprint(item)

        import_module(f"src.blueprints.{name}.routes")


app = create_app()

with app.app_context():
    register_blueprints(app)
    init_extensions(app)
