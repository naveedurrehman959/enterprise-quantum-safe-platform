# backend/app/policy_engine/routes.py
from app.algorithm_inventory.services import (
    AlgorithmInventoryService
)
from flask import Blueprint, request, jsonify

from .services import PolicyEngineService

from app.risk_assessment.services import (
    RiskAssessmentService
)

from app.audit.services import create_audit_log

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


policy_bp = Blueprint(
    "policy",
    __name__,
    url_prefix="/api/v1/policy"
)


# ---------------------------------
# Policy Status
# ---------------------------------

@policy_bp.route(
    "/status",
    methods=["GET"]
)
def policy_status():

    return jsonify(
        PolicyEngineService.get_policy()
    )

# ---------------------------------
# Enable / Disable Algorithm
# ---------------------------------

@policy_bp.route(
    "/algorithm/<int:algorithm_id>",
    methods=["PUT"]
)
@jwt_required()
def update_algorithm_policy(algorithm_id):

    data = request.get_json()

    result = AlgorithmInventoryService.set_allowed(
        algorithm_id,
        data["allowed"]
    )

    create_audit_log(
        user_id=get_jwt_identity(),
        action="POLICY_UPDATED",
        module="POLICY_ENGINE",
        status="SUCCESS",
        description=f"Algorithm {algorithm_id} allowed={data['allowed']}"
    )

    return jsonify(result)


# ---------------------------------
# List current policy algorithms
# ---------------------------------

@policy_bp.route(
    "/algorithms",
    methods=["GET"]
)
@jwt_required()
def policy_algorithms():

    return jsonify({
        "algorithms":
            AlgorithmInventoryService.list_algorithms()
    })
# ---------------------------------
# Basic Algorithm Policy Check
# ---------------------------------

@policy_bp.route(
    "/check",
    methods=["POST"]
)
def check_policy():

    data = request.get_json()

    result = PolicyEngineService.check_algorithm(
        data["algorithm"]
    )

    return jsonify(result)



# ---------------------------------
# Risk Based Policy Evaluation
# ---------------------------------

@policy_bp.route(
    "/evaluate-risk",
    methods=["POST"]
)
@jwt_required()
def evaluate_risk():

    data = request.get_json()

    algorithm = data.get(
        "algorithm"
    )


    user_id = get_jwt_identity()


    # Risk Engine Call

    risk = RiskAssessmentService.assess_algorithm(
        algorithm
    )


    # Decision Logic

    if risk["risk_level"] == "CRITICAL":

        decision = {
            "policy_action": "BLOCK",
            "allowed": False,
            "migration_required": True
        }


    elif risk["risk_level"] == "HIGH":

        decision = {
            "policy_action": "MIGRATE",
            "allowed": False,
            "migration_required": True
        }


    elif risk["risk_level"] in [
        "LOW",
        "SAFE"
    ]:

        decision = {
            "policy_action": "APPROVE",
            "allowed": True,
            "migration_required": False
        }


    else:

        decision = {
            "policy_action": "REVIEW",
            "allowed": False,
            "migration_required": True
        }



    create_audit_log(
        user_id=user_id,
        action="POLICY_RISK_EVALUATION",
        module="POLICY_ENGINE",
        status="SUCCESS",
        description=(
            f"Policy evaluation performed "
            f"for {algorithm}"
        )
    )


    return jsonify({

        "algorithm": algorithm,

        "risk_level":
            risk["risk_level"],

        "risk_score":
            risk["risk_score"],

        "quantum_vulnerable":
            risk["quantum_vulnerable"],

        "recommendation":
            risk["recommendation"],

        **decision

    }), 200
