from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from .services import DashboardService


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/v1/dashboard"
)


@dashboard_bp.route("/", methods=["GET"])
@jwt_required()
def dashboard():

    return jsonify(
        DashboardService.get_dashboard()
    )
