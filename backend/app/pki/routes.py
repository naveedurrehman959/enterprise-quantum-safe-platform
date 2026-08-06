# backend/app/pki/routes.py

from flask import (
    Blueprint,
    jsonify,
    request,
)

from flask_jwt_extended import (
    get_jwt_identity,
)

from app.auth.decorators import (
    roles_required,
)

from app.pki.services import (
    issue_certificate,
    get_certificates,
    revoke_certificate,
)


pki_bp = Blueprint(
    "pki",
    __name__,
    url_prefix="/api/v1/pki",
)


# ---------------------------------
# List Certificates
# ---------------------------------

@pki_bp.route(
    "/certificates",
    methods=["GET"]
)
@roles_required(
    "user",
    "security",
    "admin"
)
def list_certificates():

    user_id = get_jwt_identity()

    certificates = get_certificates(
        int(user_id)
    )


    return jsonify(
        {
            "certificates":
            [
                cert.to_dict()
                for cert in certificates
            ]
        }
    ), 200



# ---------------------------------
# Issue Certificate
# Security/Admin Only
# ---------------------------------
@pki_bp.route(
    "/issue",
    methods=["POST"]
)
@roles_required(
    "security",
    "admin"
)
def issue_certificate_route():

    user_id = get_jwt_identity()


    data = request.get_json() or {}



    certificate = issue_certificate(

        user_id=int(user_id),

        certificate_type=data.get(
            "type",
            "PQC-SERVER"
        ),

        algorithm=data.get(
            "algorithm",
            "ML-DSA-65"
        )

    )



    return jsonify(

        {

            "message":
            "Certificate issued successfully",


            "certificate":
            certificate.to_dict()

        }

    ), 201


# ---------------------------------
# Revoke Certificate
# Security/Admin Only
# ---------------------------------

@pki_bp.route(
    "/revoke/<serial>",
    methods=["POST"]
)
@roles_required(
    "security",
    "admin"
)
def revoke_certificate_route(serial):

    certificate = revoke_certificate(
        serial
    )


    if not certificate:

        return jsonify(
            {
                "error":
                "Certificate not found"
            }
        ),404


    return jsonify(
        {
            "message":
            "Certificate revoked",

            "serial":
            serial
        }
    ),200
