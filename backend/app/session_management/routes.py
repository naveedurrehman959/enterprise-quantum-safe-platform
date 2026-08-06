from flask import Blueprint, jsonify, request

from .services import SessionManagementService


session_bp = Blueprint(
    "sessions",
    __name__
)


@session_bp.route(
    "/sessions",
    methods=["GET"]
)
def list_sessions():

    return jsonify({
        "sessions":
        SessionManagementService.get_active_sessions()
    })


@session_bp.route(
    "/sessions/<int:session_id>",
    methods=["DELETE"]
)
def terminate_session(session_id):

    result = SessionManagementService.terminate_session(
        session_id
    )

    return jsonify(result)


@session_bp.route(
    "/sessions/logout-all",
    methods=["POST"]
)
def logout_all_sessions():

    data = request.json

    user_id = data.get("user_id")

    result = SessionManagementService.terminate_all_sessions(
        user_id
    )

    return jsonify(result)


@session_bp.route(
    "/sessions/cleanup",
    methods=["POST"]
)
def cleanup_sessions():

    result = SessionManagementService.cleanup_expired_sessions()

    return jsonify(result)
