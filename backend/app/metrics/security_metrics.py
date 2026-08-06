from datetime import datetime, timedelta

from prometheus_client import Gauge

from app.algorithm_inventory.models import AlgorithmAsset
from app.models.certificate import Certificate
from app.session_management.models import UserSession
from app.vault.services import vault_storage
from app.models.audit_logs import AuditLog


# ---------------------------------
# Certificate Metrics
# ---------------------------------

TOTAL_CERTIFICATES = Gauge(
    "total_certificates",
    "Total certificates issued",
)

ACTIVE_CERTIFICATES = Gauge(
    "active_certificates",
    "Active certificates",
)

REVOKED_CERTIFICATES = Gauge(
    "revoked_certificates",
    "Revoked certificates",
)

PQC_CERTIFICATES = Gauge(
    "pqc_certificates",
    "Quantum-safe certificates",
)

EXPIRING_CERTIFICATES = Gauge(
    "expiring_certificates",
    "Certificates nearing expiration",
)


# ---------------------------------
# Vault Metrics
# ---------------------------------

TOTAL_SECRETS = Gauge(
    "total_secrets",
    "Total secrets stored in Vault",
)

VAULT_SERVICE_STATUS = Gauge(
    "vault_service_status",
    "Vault service status (1=ACTIVE, 0=INACTIVE)",
)

CERTIFICATE_STORAGE_ENABLED = Gauge(
    "certificate_storage_enabled",
    "Certificate storage enabled",
)

KEY_ROTATION_ENABLED = Gauge(
    "key_rotation_enabled",
    "Key rotation enabled",
)


# ---------------------------------
# Compliance Metrics
# ---------------------------------

COMPLIANCE_SCORE = Gauge(
    "compliance_score",
    "Overall compliance score",
)

COMPLIANT_ASSETS = Gauge(
    "compliant_assets",
    "Number of compliant cryptographic assets",
)

NON_COMPLIANT_ASSETS = Gauge(
    "non_compliant_assets",
    "Number of non-compliant cryptographic assets",
)

SUPPORTED_FRAMEWORKS = Gauge(
    "supported_frameworks",
    "Number of supported compliance frameworks",
)

COMPLIANCE_VIOLATIONS = Gauge(
    "compliance_violations",
    "Number of compliance violations",
)


# ---------------------------------
# Session Metrics
# ---------------------------------

TOTAL_SESSIONS = Gauge(
    "total_sessions",
    "Total user sessions",
)

ACTIVE_SESSIONS_TOTAL = Gauge(
    "active_sessions_total",
    "Active user sessions",
)

EXPIRED_SESSIONS_TOTAL = Gauge(
    "expired_sessions_total",
    "Expired user sessions",
)

TERMINATED_SESSIONS_TOTAL = Gauge(
    "terminated_sessions_total",
    "Terminated user sessions",
)

CONCURRENT_USER_SESSIONS = Gauge(
    "concurrent_user_sessions",
    "Concurrent active user sessions",
)


# ---------------------------------
# Certificate Metrics Updater
# ---------------------------------

def update_certificate_metrics():

    TOTAL_CERTIFICATES.set(
        Certificate.query.count()
    )

    ACTIVE_CERTIFICATES.set(
        Certificate.query.filter_by(
            certificate_status="active"
        ).count()
    )

    REVOKED_CERTIFICATES.set(
        Certificate.query.filter_by(
            certificate_status="revoked"
        ).count()
    )

    PQC_CERTIFICATES.set(
        Certificate.query.filter(
            Certificate.algorithm.like("ML-%")
        ).count()
    )

    expiry_threshold = (
        datetime.utcnow()
        + timedelta(days=30)
    )

    EXPIRING_CERTIFICATES.set(
        Certificate.query.filter(
            Certificate.expires_at <= expiry_threshold,
            Certificate.certificate_status == "active",
        ).count()
    )


# ---------------------------------
# Vault Metrics Updater
# ---------------------------------

def update_vault_metrics():

    TOTAL_SECRETS.set(
        len(vault_storage)
    )

    VAULT_SERVICE_STATUS.set(1)

    CERTIFICATE_STORAGE_ENABLED.set(1)

    KEY_ROTATION_ENABLED.set(1)


# ---------------------------------
# Compliance Metrics Updater
# ---------------------------------

def update_compliance_metrics():

    total_assets = AlgorithmAsset.query.count()

    compliant_assets = AlgorithmAsset.query.filter_by(
        risk_level="SAFE"
    ).count()

    non_compliant_assets = (
        total_assets - compliant_assets
    )

    score = 0

    if total_assets > 0:

        score = int(
            (compliant_assets / total_assets) * 100
        )

    COMPLIANCE_SCORE.set(score)

    COMPLIANT_ASSETS.set(
        compliant_assets
    )

    NON_COMPLIANT_ASSETS.set(
        non_compliant_assets
    )

    # Supported frameworks:
    # - NIST-PQC
    # - NIST-CSF-2.0
    # - CNSA-2.0
    # - ISO-27001
    # - PCI-DSS

    SUPPORTED_FRAMEWORKS.set(5)

    COMPLIANCE_VIOLATIONS.set(
        non_compliant_assets
    )


# ---------------------------------
# Session Metrics Updater
# ---------------------------------

def update_session_metrics():

    TOTAL_SESSIONS.set(
        UserSession.query.count()
    )

    ACTIVE_SESSIONS_TOTAL.set(
        UserSession.query.filter_by(
            status="active"
        ).count()
    )

    EXPIRED_SESSIONS_TOTAL.set(
        UserSession.query.filter_by(
            status="expired"
        ).count()
    )

    TERMINATED_SESSIONS_TOTAL.set(
        UserSession.query.filter_by(
            status="terminated"
        ).count()
    )

    CONCURRENT_USER_SESSIONS.set(
        UserSession.query.filter_by(
            status="active"
        ).count()
    )
    
    # ---------------------------------
# Risk Assessment Metrics
# ---------------------------------

TOTAL_RISK_ASSETS = Gauge(
    "total_risk_assets",
    "Total cryptographic assets analyzed",
)

CRITICAL_RISK_ASSETS = Gauge(
    "critical_risk_assets",
    "Critical risk assets",
)

HIGH_RISK_ASSETS = Gauge(
    "high_risk_assets",
    "High risk assets",
)

MEDIUM_RISK_ASSETS = Gauge(
    "medium_risk_assets",
    "Medium risk assets",
)

LOW_RISK_ASSETS = Gauge(
    "low_risk_assets",
    "Low risk assets",
)

SAFE_RISK_ASSETS = Gauge(
    "safe_risk_assets",
    "Quantum-safe assets",
)

MIGRATION_REQUIRED_ASSETS = Gauge(
    "migration_required_assets",
    "Assets requiring migration",
)

RISK_SCORE = Gauge(
    "risk_score",
    "Overall platform risk score",
)
# ---------------------------------
# Risk Metrics Updater
# ---------------------------------

def update_risk_metrics():

    total = AlgorithmAsset.query.count()

    critical = AlgorithmAsset.query.filter_by(
        risk_level="CRITICAL"
    ).count()

    high = AlgorithmAsset.query.filter_by(
        risk_level="HIGH"
    ).count()

    medium = AlgorithmAsset.query.filter_by(
        risk_level="MEDIUM"
    ).count()

    low = AlgorithmAsset.query.filter_by(
        risk_level="LOW"
    ).count()

    safe = AlgorithmAsset.query.filter_by(
        risk_level="SAFE"
    ).count()

    migration_required = (
        critical +
        high +
        medium +
        low
    )

    TOTAL_RISK_ASSETS.set(total)

    CRITICAL_RISK_ASSETS.set(critical)

    HIGH_RISK_ASSETS.set(high)

    MEDIUM_RISK_ASSETS.set(medium)

    LOW_RISK_ASSETS.set(low)

    SAFE_RISK_ASSETS.set(safe)

    MIGRATION_REQUIRED_ASSETS.set(
        migration_required
    )

    score = 0

    if total > 0:

        score = int(
            (safe / total) * 100
        )

    RISK_SCORE.set(score)
# ---------------------------------
# Audit Logging Metrics
# ---------------------------------

TOTAL_AUDIT_EVENTS = Gauge(
    "total_audit_events",
    "Total audit events",
)

LOGIN_EVENTS = Gauge(
    "login_events",
    "Authentication login events",
)

FAILED_LOGIN_EVENTS = Gauge(
    "failed_login_events",
    "Failed login attempts",
)

ADMIN_ACTIONS = Gauge(
    "admin_actions",
    "Administrative actions",
)

MIGRATION_EVENTS = Gauge(
    "migration_events",
    "Cryptographic migration events",
)

POLICY_VIOLATION_EVENTS = Gauge(
    "policy_violation_events",
    "Policy violation events",
)
# ---------------------------------
# Audit Metrics Updater
# ---------------------------------

def update_audit_metrics():

    TOTAL_AUDIT_EVENTS.set(
        AuditLog.query.count()
    )


    LOGIN_EVENTS.set(
        AuditLog.query.filter_by(
            action="LOGIN"
        ).count()
    )


    FAILED_LOGIN_EVENTS.set(
        AuditLog.query.filter(
            AuditLog.action=="LOGIN",
            AuditLog.status=="FAILED"
        ).count()
    )


    ADMIN_ACTIONS.set(
        AuditLog.query.filter(
            AuditLog.user_id.isnot(None)
        ).count()
    )


    MIGRATION_EVENTS.set(
        AuditLog.query.filter(
            AuditLog.module.ilike("%MIGRATION%")
        ).count()
    )


    POLICY_VIOLATION_EVENTS.set(
        AuditLog.query.filter(
            AuditLog.module.ilike("%POLICY%")
        ).count()
    )
