# backend/app/audit/services.py

from app.extensions import db
from app.models.audit_logs import AuditLog


def create_audit_log(
    user_id,
    action,
    module,
    status,
    description,
):
    """
    Create and store an audit log entry.
    """

    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        module=module,
        status=status,
        description=description,
    )

    db.session.add(audit_log)

    return audit_log
