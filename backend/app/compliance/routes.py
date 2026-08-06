# backend/app/compliance/routes.py

from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    get_jwt_identity,
)

from app.auth.decorators import (
    roles_required,
)

from .schemas import (
    ComplianceFrameworkSchema,
)

from .services import (
    ComplianceService,
)


compliance_bp = Blueprint(
    "compliance",
    __name__,
    url_prefix="/api/v1/compliance",
)


# ---------------------------------
# Compliance Status
# ---------------------------------

@compliance_bp.route(
    "/status",
    methods=["GET"]
)
@roles_required(
    "user",
    "security",
    "admin",
)
def compliance_status():

    user_id = get_jwt_identity()

    return jsonify(
        ComplianceService.get_compliance_status(
            user_id
        )
    ), 200



# ---------------------------------
# Supported Frameworks
# ---------------------------------

@compliance_bp.route(
    "/frameworks",
    methods=["GET"],
)
@roles_required(
    "user",
    "security",
    "admin",
)
def frameworks():

    user_id = get_jwt_identity()

    return jsonify(
        ComplianceService.get_supported_frameworks(
            user_id
        )
    ), 200



# ---------------------------------
# Validate Compliance Framework
# ---------------------------------

@compliance_bp.route(
    "/validate",
    methods=["POST"],
)
@roles_required(
    "security",
    "admin",
)
def validate():

    data = request.get_json()


    errors = (
        ComplianceFrameworkSchema()
        .validate(data)
    )


    if errors:

        return jsonify(errors), 400



    user_id = get_jwt_identity()


    return jsonify(

        ComplianceService.validate_framework(

            framework=data["framework"],

            algorithm=data.get(
                "algorithm"
            ),

            user_id=user_id

        )

    ), 200



# ---------------------------------
# Compliance Dashboard
# ---------------------------------

@compliance_bp.route(
    "/dashboard",
    methods=["GET"]
)
@roles_required(
    "user",
    "security",
    "admin"
)
def dashboard():

    user_id = get_jwt_identity()


    return jsonify(

        ComplianceService.compliance_dashboard(
            user_id
        )

    ), 200



# ---------------------------------
# Compliance Report
# ---------------------------------

@compliance_bp.route(
    "/report",
    methods=["GET"]
)
@roles_required(
    "security",
    "admin"
)
def report():

    user_id = get_jwt_identity()


    return jsonify(

        ComplianceService.generate_report(
            user_id
        )

    ), 200
