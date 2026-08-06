from flask import Blueprint, request, jsonify

from .services import AlgorithmInventoryService


inventory_bp = Blueprint(
    "inventory",
    __name__,
    url_prefix="/api/v1/inventory"
)


# ----------------------------------------
# List all algorithms
# ----------------------------------------

@inventory_bp.route(
    "/algorithms",
    methods=["GET"]
)
def list_algorithms():

    return jsonify({
        "algorithms":
            AlgorithmInventoryService.list_algorithms()
    })


# ----------------------------------------
# Inventory summary
# ----------------------------------------

@inventory_bp.route(
    "/summary",
    methods=["GET"]
)
def inventory_summary():

    return jsonify(
        AlgorithmInventoryService.get_summary()
    )


# ----------------------------------------
# Add new algorithm
# ----------------------------------------

@inventory_bp.route(
    "/algorithms",
    methods=["POST"]
)
def add_algorithm():

    data = request.get_json()

    result = AlgorithmInventoryService.create_algorithm(
        data
    )

    return jsonify(result), 201


# ----------------------------------------
# Allow / Disable algorithm
# Used by Policy Engine
# ----------------------------------------

@inventory_bp.route(
    "/<int:algorithm_id>/allow",
    methods=["PUT"]
)
def allow_algorithm(algorithm_id):

    data = request.get_json()

    result = AlgorithmInventoryService.set_allowed(
        algorithm_id,
        data["allowed"]
    )

    return jsonify(result)


# ----------------------------------------
# Activate / Deactivate algorithm
# ----------------------------------------

@inventory_bp.route(
    "/<int:algorithm_id>/active",
    methods=["PUT"]
)
def activate_algorithm(algorithm_id):

    data = request.get_json()

    result = AlgorithmInventoryService.set_active(
        algorithm_id,
        data["active"]
    )

    return jsonify(result)


# ----------------------------------------
# Change deployment mode
# Used by Crypto Agility
# ----------------------------------------

@inventory_bp.route(
    "/deployment-mode",
    methods=["PUT"]
)
def deployment_mode():

    data = request.get_json()

    result = AlgorithmInventoryService.set_deployment_mode(
        data["mode"]
    )

    return jsonify(result)
