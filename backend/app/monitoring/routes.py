# backend/app/monitoring/routes.py

from flask import Blueprint, jsonify

from .services import MonitoringService

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

monitoring_bp = Blueprint(
    "monitoring",
    __name__,
    url_prefix="/api/v1/monitoring"
)


# ---------------------------------
# Platform Status
# ---------------------------------

@monitoring_bp.route(
    "/status",
    methods=["GET"]
)
def status():

    return jsonify(
        MonitoringService.get_platform_status()
    ), 200



# ---------------------------------
# System Health
# ---------------------------------

@monitoring_bp.route(
    "/system-health",
    methods=["GET"]
)
def system_health():

    return jsonify(
        MonitoringService.get_system_health()
    ), 200



# ---------------------------------
# Crypto Metrics
# ---------------------------------

@monitoring_bp.route(
    "/crypto-metrics",
    methods=["GET"]
)
def crypto_metrics():

    return jsonify(
        MonitoringService.get_crypto_metrics()
    ), 200



# ---------------------------------
# Security Audit Events
# ---------------------------------

@monitoring_bp.route(
    "/security-events",
    methods=["GET"]
)
def security_events():

    return jsonify(
        MonitoringService.get_security_events()
    ), 200



# ---------------------------------
# Main Dashboard
# ---------------------------------

@monitoring_bp.route(
    "/dashboard",
    methods=["GET"]
)
def dashboard():

    return jsonify(
        MonitoringService.get_dashboard()
    ), 200



# ---------------------------------
# Quantum Readiness Dashboard
# ---------------------------------

@monitoring_bp.route(
    "/quantum-readiness",
    methods=["GET"]
)
def quantum_readiness():

    return jsonify(
        MonitoringService.quantum_readiness()
    ), 200



# ---------------------------------
# Service Health Dashboard
# ---------------------------------

@monitoring_bp.route(
    "/services",
    methods=["GET"]
)
def services():

    return jsonify(
        MonitoringService.services_status()
    ), 200
# ---------------------------------
# PKI Monitoring
# ---------------------------------

@monitoring_bp.route(
    "/pki-status",
    methods=["GET"]
)
def pki_status():

    return jsonify(
        MonitoringService.get_pki_status()
    ), 200

@monitoring_bp.route("/platform-status", methods=["GET"])
@jwt_required()
def platform_status():

    return jsonify(
        MonitoringService.get_platform_status()
    ), 200

# ---------------------------------
# Vault Monitoring
# ---------------------------------

@monitoring_bp.route(
    "/vault-status",
    methods=["GET"]
)
def vault_status():

    return jsonify(
        MonitoringService.get_vault_status()
    ), 200
