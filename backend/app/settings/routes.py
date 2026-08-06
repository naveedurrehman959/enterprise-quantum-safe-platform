from flask import Blueprint
from flask import jsonify
from flask import request

from .services import SettingsService

settings_bp = Blueprint(
    "settings",
    __name__,
    url_prefix="/api/v1/settings"
)


@settings_bp.route(
    "",
    methods=["GET"]
)
def get_settings():

    return jsonify(
        SettingsService.get_settings()
    )


@settings_bp.route(
    "",
    methods=["PUT"]
)
def update_settings():

    data = request.get_json()

    return jsonify(
        SettingsService.update_settings(data)
    )
