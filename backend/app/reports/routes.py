from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from .services import ReportService

reports_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/api/v1/reports",
)


@reports_bp.route("/", methods=["GET"])
@jwt_required()
def get_report():
    return jsonify(
        ReportService.generate_report()
    ), 200


@reports_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    return jsonify(
        ReportService.get_summary()
    ), 200


@reports_bp.route("/risk", methods=["GET"])
@jwt_required()
def risk():
    return jsonify(
        ReportService.get_risk_report()
    ), 200


@reports_bp.route("/compliance", methods=["GET"])
@jwt_required()
def compliance():
    return jsonify(
        ReportService.get_compliance_report()
    ), 200


@reports_bp.route("/migration", methods=["GET"])
@jwt_required()
def migration():
    return jsonify(
        ReportService.get_migration_report()
    ), 200


@reports_bp.route("/audit", methods=["GET"])
@jwt_required()
def audit():
    return jsonify(
        ReportService.get_audit_report()
    ), 200


@reports_bp.route("/certificates", methods=["GET"])
@jwt_required()
def certificates():
    return jsonify(
        ReportService.get_certificate_report()
    ), 200


@reports_bp.route("/export/pdf", methods=["GET"])
@jwt_required()
def export_pdf():
    return jsonify(
        ReportService.export_pdf()
    ), 200


@reports_bp.route("/export/csv", methods=["GET"])
@jwt_required()
def export_csv():
    return jsonify(
        ReportService.export_csv()
    ), 200
