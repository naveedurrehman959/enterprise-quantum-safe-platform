from app.models.user import User
from app.models.audit_logs import AuditLog
from app.algorithm_inventory.models import AlgorithmAsset
from app.models.certificate import Certificate


class SearchService:

    @staticmethod
    def search(query):

        results = {
            "users": [],
            "algorithms": [],
            "certificates": [],
            "audit_logs": []
        }

        # Users
        users = User.query.filter(
            User.username.ilike(f"%{query}%")
        ).all()

        results["users"] = [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": u.role
            }
            for u in users
        ]

        # Algorithm Inventory
        assets = AlgorithmAsset.query.filter(
            AlgorithmAsset.asset_name.ilike(f"%{query}%")
        ).all()

        results["algorithms"] = [
            a.to_dict()
            for a in assets
        ]

        # Certificates
        certs = Certificate.query.filter(
            Certificate.certificate_serial_number.ilike(f"%{query}%")
        ).all()

        results["certificates"] = [
            c.to_dict()
            for c in certs
        ]

        # Audit Logs
        logs = AuditLog.query.filter(
            AuditLog.description.ilike(f"%{query}%")
        ).all()

        results["audit_logs"] = [
            l.to_dict()
            for l in logs
        ]

        return results
