from flask import Blueprint

site_bp = Blueprint(
    "site",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

from src.blueprints.site import routes  # noqa: E402,F401
