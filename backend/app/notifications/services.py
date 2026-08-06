from app.models.audit_logs import AuditLog


class NotificationService:

    @staticmethod
    def get_notifications():

        logs = (
            AuditLog.query
            .order_by(AuditLog.timestamp.desc())
            .limit(10)
            .all()
        )

        notifications = []

        for log in logs:

            notifications.append({
                "id": log.id,
                "title": log.action,
                "message": log.description,
                "module": log.module,
                "status": log.status,
                "timestamp": (
                    log.timestamp.isoformat()
                    if log.timestamp
                    else None
                )
            })

        return notifications
