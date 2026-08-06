from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.models.audit_logs import AuditLog


audit_bp = Blueprint(
    "audit",
    __name__,
    url_prefix="/api/v1/audit"
)


@audit_bp.route("/logs", methods=["GET"])
@jwt_required()
def get_audit_logs():

    logs = AuditLog.query.order_by(
        AuditLog.id.desc()
    ).all()


    return jsonify(
        {
            "logs":[
                log.to_dict()
                for log in logs
            ]
        }
    ),200
