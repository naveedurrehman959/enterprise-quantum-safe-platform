# backend/app/pki/services.py

from datetime import datetime, timedelta
import uuid

from app.extensions import db
from app.models.certificate import Certificate

from app.risk_assessment.services import (
    RiskAssessmentService
)

from app.policy_engine.services import (
    PolicyEngineService
)

from app.crypto_agility.services import (
    CryptoAgilityService
)


# ---------------------------------
# Issue Risk-Aware Certificate
# ---------------------------------

def issue_certificate(
    user_id,
    certificate_type="PQC-SERVER",
    algorithm="ML-DSA-65"
):

    requested_algorithm = algorithm.upper()


    # -----------------------------
    # Risk Assessment
    # -----------------------------

    risk = RiskAssessmentService.assess_algorithm(
        requested_algorithm
    )


    risk_level = risk.get(
        "risk_level",
        "UNKNOWN"
    )


    risk_score = risk.get(
        "risk_score",
        50
    )


    quantum_vulnerable = risk.get(
        "quantum_vulnerable"
    )


    recommendation = risk.get(
        "recommendation",
        requested_algorithm
    )


    # -----------------------------
    # Policy Decision
    # -----------------------------

    policy = PolicyEngineService.check_algorithm(
        requested_algorithm
    )


    policy_status = policy.get(
        "status"
    )


    final_algorithm = requested_algorithm

    migration_status = "COMPLETED"



    # -----------------------------
    # Migration Decision
    # -----------------------------

    if policy_status in [

        "BLOCKED",
        "MIGRATION_REQUIRED"

    ] or risk_level in [

        "HIGH",
        "CRITICAL"

    ]:


        migration = CryptoAgilityService.select_algorithm(
            requested_algorithm
        )


        final_algorithm = migration.get(
            "recommended_algorithm",
            "ECDHE + ML-KEM-768"
        )


        migration_status = "REQUIRED"



    elif policy_status == "CONDITIONAL":


        final_algorithm = (
            "ECDHE + ML-KEM-768"
        )


        migration_status = "HYBRID"



    # -----------------------------
    # Certificate Creation
    # -----------------------------

    serial_number = str(
        uuid.uuid4()
    )


    if "KEM" in final_algorithm:

        category = "KEY_ENCAPSULATION"

    else:

        category = "DIGITAL_SIGNATURE"



    certificate = Certificate(

        user_id=user_id,

        certificate_serial_number=serial_number,


        certificate_type=certificate_type,


        certificate_reference=(
            f"/vault/certificates/{serial_number}.pem"
        ),


        algorithm=final_algorithm,


        algorithm_category=category,


        risk_level=risk_level,


        migration_status=migration_status,


        recommended_algorithm=recommendation,


        certificate_status="active",


        issued_at=datetime.utcnow(),


        expires_at=(
            datetime.utcnow()
            +
            timedelta(days=365)
        )

    )


    db.session.add(
        certificate
    )

    db.session.commit()


    return certificate





# ---------------------------------
# List Certificates
# ---------------------------------

def get_certificates(user_id=None):

    if user_id:

        return Certificate.query.filter_by(
            user_id=user_id
        ).all()


    return Certificate.query.all()




# ---------------------------------
# Revoke Certificate
# ---------------------------------

def revoke_certificate(serial_number):


    certificate = Certificate.query.filter_by(
        certificate_serial_number=serial_number
    ).first()


    if not certificate:

        return None



    certificate.certificate_status = "revoked"


    db.session.commit()


    return certificate
