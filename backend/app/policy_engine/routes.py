from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.audit.services import create_audit_log

from .services import PolicyEngineService


policy_bp = Blueprint(
    "policy",
    __name__,
    url_prefix="/api/v1/policy"
)


# ==========================================================
# POLICY STATUS
# ==========================================================

@policy_bp.route(
    "/status",
    methods=["GET"]
)
@jwt_required()
def policy_status():

    return jsonify(
        PolicyEngineService.get_policy()
    ), 200


# ==========================================================
# LIST POLICIES
# ==========================================================

@policy_bp.route(
    "/algorithms",
    methods=["GET"]
)
@jwt_required()
def policy_algorithms():

    return jsonify({
        "algorithms":
            PolicyEngineService.list_policies()
    }), 200


# ==========================================================
# UPDATE POLICY
# ==========================================================

@policy_bp.route(
    "/algorithm/<string:algorithm_name>",
    methods=["PUT"]
)
@jwt_required()
def update_algorithm_policy(algorithm_name):

    data = request.get_json() or {}

    try:

        result = PolicyEngineService.update_policy(
            algorithm_name=algorithm_name,
            enabled=data.get("enabled"),
            deployment_mode=data.get(
                "deployment_mode"
            ),
            enforcement_action=data.get(
                "enforcement_action"
            )
        )

        create_audit_log(
            user_id=get_jwt_identity(),
            action="POLICY_UPDATED",
            module="POLICY_ENGINE",
            status="SUCCESS",
            description=(
                f"Policy updated for "
                f"{algorithm_name}"
            )
        )

        return jsonify(result), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except Exception as error:

        return jsonify({
            "error":
                "Unable to update policy.",
            "details":
                str(error)
        }), 500


# ==========================================================
# BASIC POLICY CHECK
# ==========================================================

@policy_bp.route(
    "/check",
    methods=["POST"]
)
@jwt_required()
def check_policy():

    data = request.get_json() or {}

    algorithm = data.get("algorithm")

    if not algorithm:

        return jsonify({
            "error":
                "algorithm is required"
        }), 400

    result = PolicyEngineService.check_algorithm(
        algorithm
    )

    return jsonify(result), 200


# ==========================================================
# RISK + POLICY EVALUATION
# ==========================================================

@policy_bp.route(
    "/evaluate-risk",
    methods=["POST"]
)
@jwt_required()
def evaluate_risk():

    data = request.get_json() or {}

    algorithm = data.get("algorithm")

    if not algorithm:

        return jsonify({
            "error":
                "algorithm is required"
        }), 400

    result = PolicyEngineService.evaluate_policy(
        algorithm
    )

    create_audit_log(
        user_id=get_jwt_identity(),
        action="POLICY_RISK_EVALUATION",
        module="POLICY_ENGINE",
        status="SUCCESS",
        description=(
            f"Policy evaluation performed "
            f"for {algorithm}"
        )
    )

    return jsonify(result), 200
