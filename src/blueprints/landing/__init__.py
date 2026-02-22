from flask import Blueprint

landing = Blueprint("landing", __name__, template_folder="templates")

from src.blueprints.landing import routes  # noqa: E402,F401
