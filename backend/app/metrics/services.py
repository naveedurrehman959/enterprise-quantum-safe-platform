# backend/app/metrics/services.py

import psutil

from app.algorithm_inventory.models import AlgorithmAsset

from .prometheus_metrics import CPU_USAGE
from .prometheus_metrics import MEMORY_USAGE
from .prometheus_metrics import DISK_USAGE
from .prometheus_metrics import TOTAL_ALGORITHMS
from .prometheus_metrics import SAFE_ALGORITHMS
from .prometheus_metrics import VULNERABLE_ALGORITHMS
from .prometheus_metrics import QUANTUM_READINESS_SCORE

from .security_metrics import (
    update_certificate_metrics,
    update_vault_metrics,
    update_compliance_metrics,
    update_session_metrics,
    update_risk_metrics,
    update_audit_metrics,
)


class MetricsService:

    @staticmethod
    def update_metrics():

        # ---------------------------------
        # System Metrics
        # ---------------------------------

        CPU_USAGE.set(
            psutil.cpu_percent()
        )

        MEMORY_USAGE.set(
            psutil.virtual_memory().percent
        )

        DISK_USAGE.set(
            psutil.disk_usage("/").percent
        )

        # ---------------------------------
        # Algorithm Metrics
        # ---------------------------------

        total = AlgorithmAsset.query.count()

        safe = AlgorithmAsset.query.filter_by(
            risk_level="SAFE"
        ).count()

        vulnerable = total - safe

        TOTAL_ALGORITHMS.set(total)

        SAFE_ALGORITHMS.set(safe)

        VULNERABLE_ALGORITHMS.set(
            vulnerable
        )

        score = 0

        if total > 0:

            score = int(
                (safe / total) * 100
            )

        QUANTUM_READINESS_SCORE.set(
            score
        )

        # ---------------------------------
        # Certificate Metrics
        # ---------------------------------

        update_certificate_metrics()

        # ---------------------------------
        # Vault Metrics
        # ---------------------------------

        update_vault_metrics()
        # ---------------------------------
        # Compliance Metrics
        # ---------------------------------

        update_compliance_metrics()
        # ---------------------------------
        # Session Metrics
        # ---------------------------------

        update_session_metrics()
        # ---------------------------------
        # Risk Metrics
        # ---------------------------------

        update_risk_metrics()
        # ---------------------------------
        # Audit Metrics
        # ---------------------------------

        update_audit_metrics()
