from flask import Blueprint, jsonify, request

from .services import RiskAssessmentService


risk_bp = Blueprint(
    "risk",
    __name__,
    url_prefix="/api/v1/risk-assessment"
)



@risk_bp.route(
    "/status",
    methods=["GET"]
)
def status():


    return jsonify({

        "engine":"ACTIVE",

        "quantum_threat_detection":
        "ENABLED"

    })




@risk_bp.route(
    "/assess",
    methods=["POST"]
)
def assess():


    data=request.json


    algorithm=data.get(
        "algorithm"
    )


    result = (
        RiskAssessmentService
        .assess_algorithm(
            algorithm
        )
    )


    return jsonify(result)





@risk_bp.route(
    "/inventory",
    methods=["GET"]
)
def inventory():


    return jsonify({

        "vulnerable_algorithms":[

            "RSA",
            "ECDSA",
            "SHA1",
            "DES"

        ],


        "quantum_safe_algorithms":[

            "ML-KEM-768",
            "ML-DSA-65",
            "AES-256-GCM"

        ]

    })
