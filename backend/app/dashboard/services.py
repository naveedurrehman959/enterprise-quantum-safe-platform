from app.models.user import User
from app.models.certificate import Certificate

from app.models.audit_logs import AuditLog
from app.algorithm_inventory.models import AlgorithmAsset

class DashboardService:

    @staticmethod
    def get_dashboard():

        total_users = User.query.count()

        total_certificates = Certificate.query.count()

        total_assets = AlgorithmAsset.query.count()

        total_logs = AuditLog.query.count()

        vulnerable = AlgorithmAsset.query.filter(
            AlgorithmAsset.risk_level != "SAFE"
        ).count()

        return {
            "users": total_users,
            "certificates": total_certificates,
            "algorithm_assets": total_assets,
            "audit_logs": total_logs,
            "vulnerable_assets": vulnerable,
            "security_score": max(
                0,
                100 - vulnerable * 10
            )
        }
