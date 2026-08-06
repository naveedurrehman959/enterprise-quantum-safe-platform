from flask import Blueprint, request, jsonify

from .services import MigrationEngineService


migration_bp = Blueprint(
    "migration",
    __name__,
    url_prefix="/api/v1/migration"
)



@migration_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze_migration():

    data = request.get_json()

    result = MigrationEngineService.analyze_migration(
        data
    )

    return jsonify(result), 200


@migration_bp.route(
    "/status",
    methods=["GET"]
)
def migration_status():

    result = {
        "migration_engine": "active",
        "status": "operational",
        "supported_modes": [
            "legacy",
            "hybrid",
            "pure_pqc"
        ],
        "target_algorithms": [
            "ML-KEM-768",
            "ML-DSA-65",
            "AES-256-GCM"
        ]
    }

    return jsonify(result),200
@migration_bp.route(
    "/plan",
    methods=["POST"]
)
def migration_plan():

    data = request.get_json()

    result = MigrationEngineService.generate_plan(
        data.get("algorithm")
    )

    return jsonify(result), 200



@migration_bp.route(
    "/report",
    methods=["GET"]
)
def migration_report():

    result = MigrationEngineService.migration_report()

    return jsonify(result), 200
