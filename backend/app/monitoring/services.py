# backend/app/monitoring/services.py

from datetime import datetime
import psutil

from app.vault.services import vault_storage
from app.models.user import User
from app.session_management.models import UserSession
from app.models.certificate import Certificate
from app.models.audit_logs import AuditLog
from app.algorithm_inventory.models import AlgorithmAsset

from app.risk_assessment.services import (
    RiskAssessmentService,
)


class MonitoringService:

    # ---------------------------------
    # System Health Monitoring
    # ---------------------------------

    @staticmethod
    def get_system_health():

        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent,
            "timestamp": datetime.utcnow().isoformat(),
        }

    # ---------------------------------
    # Platform Service Status
    # ---------------------------------

    @staticmethod
    def get_platform_status():

        return {
            "status": "healthy",
            "services": {
                "authentication": "running",
                "crypto_engine": "running",
                "pki": "running",
                "vault": "running",
                "compliance": "running",
                "risk_assessment": "running",
                "policy_engine": "running",
                "migration_engine": "running",
                "monitoring": "running",
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

    # ---------------------------------
    # Crypto Metrics
    # ---------------------------------

    @staticmethod
    def get_crypto_metrics():

        total_algorithms = AlgorithmAsset.query.count()

        pqc_algorithms = (
            AlgorithmAsset.query.filter(
                AlgorithmAsset.algorithm_name.like("ML-%")
            ).count()
        )

        return {
            "total_algorithms": total_algorithms,
            "pqc_algorithms": pqc_algorithms,
            "classical_algorithms": total_algorithms - pqc_algorithms,
            "hybrid_encryption": {
                "ECDHE+ML-KEM": "enabled",
            },
            "supported_algorithms": [
                "ML-KEM",
                "ML-DSA",
                "AES-256-GCM",
                "SHA-3",
            ],
        }

    # ---------------------------------
    # Security Events
    # ---------------------------------

    @staticmethod
    def get_security_events():

        logs = (
            AuditLog.query.order_by(AuditLog.timestamp.desc())
            .limit(10)
            .all()
        )

        events = []

        for log in logs:

            events.append(
                {
                    "user_id": log.user_id,
                    "action": log.action,
                    "module": log.module,
                    "status": log.status,
                    "description": log.description,
                    "timestamp": (
                        log.timestamp.isoformat()
                        if log.timestamp
                        else None
                    ),
                }
            )

        return {
            "total": len(events),
            "events": events,
        }

    # ---------------------------------
    # Quantum Readiness Dashboard
    # ---------------------------------

    @staticmethod
    def quantum_readiness():

        assets = AlgorithmAsset.query.all()

        summary = {
            "total": len(assets),
            "safe": 0,
            "vulnerable": 0,
        }

        risks = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "SAFE": 0,
        }

        for asset in assets:

            result = RiskAssessmentService.assess_algorithm(
                asset.algorithm_name
            )

            level = result["risk_level"]

            if level == "SAFE":
                summary["safe"] += 1
            else:
                summary["vulnerable"] += 1

            if level in risks:
                risks[level] += 1

        score = 100

        if summary["total"] > 0:
            score = int(
                (summary["safe"] / summary["total"]) * 100
            )

        return {
            "quantum_readiness_score": score,
            "status": (
                "READY"
                if score == 100
                else "PARTIALLY_READY"
            ),
            "assets": summary,
            "risk_summary": risks,
            "migration_required": summary["vulnerable"] > 0,
            "recommendation": (
                "Deploy Hybrid ECDHE + ML-KEM migration"
                if summary["vulnerable"]
                else "Infrastructure is quantum safe"
            ),
            "timestamp": datetime.utcnow().isoformat(),
        }

    # ---------------------------------
    # Main Dashboard
    # ---------------------------------

    @staticmethod
    def get_dashboard():

        readiness = MonitoringService.quantum_readiness()

        return {
            "users": User.query.count(),
            "active_sessions": UserSession.query.count(),
            "certificates": Certificate.query.count(),
            "security_alerts": AuditLog.query.filter_by(
                status="FAILED"
            ).count(),
            "security_score": readiness[
                "quantum_readiness_score"
            ],
            "quantum_readiness_score": readiness[
                "quantum_readiness_score"
            ],
            "safe_assets": readiness["assets"]["safe"],
            "vulnerable_assets": readiness["assets"][
                "vulnerable"
            ],
            "crypto_status": "healthy",
            "compliance_status": "healthy",
            "vault_status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
        }

    # ---------------------------------
    # Service Monitoring
    # ---------------------------------

    @staticmethod
    def services_status():

        return {
            "authentication": "RUNNING",
            "crypto_engine": "RUNNING",
            "risk_engine": "RUNNING",
            "policy_engine": "RUNNING",
            "migration_engine": "RUNNING",
            "pki": "RUNNING",
            "vault": "RUNNING",
        }

    # ---------------------------------
    # PKI Certificate Monitoring
    # ---------------------------------

    @staticmethod
    def get_pki_status():

        certificates = Certificate.query.all()

        total = len(certificates)
        pqc = 0
        classical = 0
        expired = 0

        now = datetime.utcnow()

        for cert in certificates:

            if cert.algorithm and "ML-" in cert.algorithm:
                pqc += 1
            else:
                classical += 1

            if cert.expires_at and cert.expires_at < now:
                expired += 1

        return {
            "total_certificates": total,
            "pqc_certificates": pqc,
            "classical_certificates": classical,
            "expired_certificates": expired,
            "certificate_health": (
                "GOOD"
                if expired == 0
                else "WARNING"
            ),
            "timestamp": datetime.utcnow().isoformat(),
        }

    # ---------------------------------
    # Vault Monitoring
    # ---------------------------------

    @staticmethod
    def get_vault_status():

        return {
            "vault_service": "ACTIVE",
            "secret_engine": "KV-V2",
            "stored_secrets": len(vault_storage),
            "encryption": "AES-256-GCM",
            "key_management": "ENABLED",
            "key_rotation": "ENABLED",
            "status": "READY",
            "timestamp": datetime.utcnow().isoformat(),
        }
