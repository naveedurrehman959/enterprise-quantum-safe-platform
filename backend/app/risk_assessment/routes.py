# backend/app/risk_assessment/routes.py


from flask import Blueprint,request,jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.auth.decorators import roles_required

from app.audit.services import create_audit_log

from .services import RiskAssessmentService

from .schemas import RiskAssessmentSchema



risk_bp = Blueprint(
    "risk",
    __name__,
    url_prefix="/api/v1/risk"
)



@risk_bp.route(
    "/status",
    methods=["GET"]
)
@jwt_required()
def status():

    return jsonify(
        RiskAssessmentService.get_status()
    )




@risk_bp.route(
    "/analyze",
    methods=["POST"]
)
@jwt_required()
@roles_required(
    "security_analyst",
    "admin"
)
def analyze_algorithm():


    data=request.get_json()


    errors=RiskAssessmentSchema().validate(
        data
    )


    if errors:

        return jsonify(errors),400



    user_id=get_jwt_identity()



    result=RiskAssessmentService.assess_algorithm(
        data["algorithm"]
    )



    create_audit_log(

        user_id=user_id,

        action="ANALYZE_ALGORITHM",

        module="RISK_ASSESSMENT",

        status="SUCCESS",

        description=
        f"Risk analysis performed for {data['algorithm']}"

    )


    return jsonify(result),200





@risk_bp.route(
    "/assessment",
    methods=["GET"]
)
@jwt_required()
def assessment():


    return jsonify(

        RiskAssessmentService.assess_inventory()

    )





@risk_bp.route(
    "/inventory",
    methods=["GET"]
)
@jwt_required()
def inventory():


    return jsonify(

        RiskAssessmentService.inventory()

    )
