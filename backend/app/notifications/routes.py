from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from .services import NotificationService

notifications_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/api/v1/notifications"
)


@notifications_bp.route("/", methods=["GET"])
@jwt_required()
def notification_status():

    return jsonify({
        "notifications":
        NotificationService.get_notifications()
    }), 200
