from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from .services import SearchService

search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/api/v1/search"
)


@search_bp.route("/", methods=["GET"])
@jwt_required()
def search():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "users": [],
            "algorithms": [],
            "certificates": [],
            "audit_logs": []
        }), 200

    results = SearchService.search(query)

    return jsonify(results), 200
