"""
Business Orchestration Layer

Workflow:

Request
   ↓
DNS Resolver
   ↓
TLS Scanner
   ↓
Certificate Parser
   ↓
Database
   ↓
Algorithm Inventory
   ↓
Risk Assessment
   ↓
Policy Engine
   ↓
Migration Engine
   ↓
Notification Center
   ↓
Audit Logs
"""

from datetime import datetime
import logging

from app import db

from app.asset_discovery.models import DiscoveredAsset

from app.asset_discovery.dns import DNSResolver
from app.asset_discovery.scanner import TLSScanner
from app.asset_discovery.certificate_parser import CertificateParser


# Security Services

from app.algorithm_inventory.services import (
    AlgorithmInventoryService
)

from app.risk_assessment.services import (
    RiskAssessmentService
)

from app.policy_engine.services import (
    PolicyEngineService
)


# Optional integrations
try:
    from app.migration_engine.services import (
        MigrationEngineService
    )
except Exception:
    MigrationEngineService = None


try:
    from app.notification.services import (
        NotificationService
    )
except Exception:
    NotificationService = None


try:
    from app.audit.services import (
        AuditService
    )
except Exception:
    AuditService = None


logger = logging.getLogger(__name__)


class AssetDiscoveryService:


    @staticmethod
    def scan_asset(target: str, port: int = 443):

        """
        Complete enterprise discovery workflow.
        """

        try:

            # --------------------------------
            # DNS Resolution
            # --------------------------------

            host = DNSResolver.resolve(target)


            # --------------------------------
            # TLS Scan
            # --------------------------------

            scan = TLSScanner.scan(
                hostname=host["hostname"],
                ip_address=host["ip_address"],
                port=port
            )


            # --------------------------------
            # Certificate Parsing
            # --------------------------------

            cert = CertificateParser.parse(
                scan["certificate_der"]
            )


            algorithm = cert.get(
                "public_key_algorithm"
            )


            # --------------------------------
            # Prevent Duplicate Assets
            # --------------------------------

            asset = DiscoveredAsset.query.filter_by(
                hostname=host["hostname"],
                port=port
            ).first()



            if asset:

                logger.info(
                    "Updating existing asset %s",
                    target
                )

            else:

                asset = DiscoveredAsset()




            # --------------------------------
            # Update Asset Information
            # --------------------------------

            asset.hostname = host["hostname"]

            asset.ip_address = host["ip_address"]

            asset.port = port


            asset.tls_version = (
                scan.get("tls_version")
            )

            asset.cipher_suite = (
                scan.get("cipher_suite")
            )


            asset.public_key_algorithm = algorithm

            asset.key_size = (
                cert.get("key_size")
            )


            asset.signature_algorithm = (
                cert.get(
                    "signature_algorithm"
                )
            )


            asset.issuer = cert.get(
                "issuer"
            )

            asset.subject = cert.get(
                "subject"
            )

            asset.serial_number = cert.get(
                "serial_number"
            )


            asset.fingerprint_sha256 = (
                cert.get(
                    "fingerprint_sha256"
                )
            )


            asset.valid_from = (
                cert.get("valid_from")
            )


            asset.valid_to = (
                cert.get("valid_to")
            )


            asset.scan_status = "RUNNING"

            asset.last_scanned = (
                datetime.utcnow()
            )


            db.session.add(asset)

            db.session.commit()



            # --------------------------------
            # Algorithm Inventory
            # --------------------------------

            try:

                AlgorithmInventoryService.auto_register_algorithm(
                    algorithm_name=algorithm,
                    key_size=asset.key_size
                )

            except Exception as e:

                logger.error(
                    "Inventory update failed: %s",
                    e
                )



            # --------------------------------
            # Risk Assessment
            # --------------------------------

            try:

                risk = (
                    RiskAssessmentService
                    .assess_algorithm(
                        algorithm
                    )
                )


                asset.risk_level = (
                    risk.get(
                        "risk_level",
                        "UNKNOWN"
                    )
                )


                asset.risk_score = (
                    risk.get(
                        "risk_score",
                        0
                    )
                )


                asset.recommended_algorithm = (
                    risk.get(
                        "recommended_algorithm"
                    )
                )


            except Exception as e:

                logger.error(
                    "Risk assessment failed: %s",
                    e
                )

                asset.risk_level = "UNKNOWN"



            # --------------------------------
            # Policy Evaluation
            # --------------------------------

            try:

                policy = (
                    PolicyEngineService
                    .evaluate_policy(
                        algorithm
                    )
                )


                asset.policy_decision = (
                    policy.get(
                        "decision",
                        "UNKNOWN"
                    )
                )


                asset.migration_required = (
                    policy.get(
                        "migration_required",
                        False
                    )
                )


            except Exception as e:

                logger.error(
                    "Policy evaluation failed: %s",
                    e
                )



            # --------------------------------
            # Migration Engine
            # --------------------------------

            if (
                asset.migration_required
                and MigrationEngineService
            ):

                try:

                    MigrationEngineService.create_plan(
                        asset_id=asset.id,
                        target_algorithm=
                        asset.recommended_algorithm
                    )


                except Exception as e:

                    logger.error(
                        "Migration plan failed: %s",
                        e
                    )



            # --------------------------------
            # Notifications
            # --------------------------------

            if (
                asset.risk_level == "CRITICAL"
                and NotificationService
            ):

                try:

                    NotificationService.send(
                        title=
                        "Critical Quantum Risk Detected",

                        message=
                        f"{asset.hostname} uses {algorithm}"
                    )

                except Exception as e:

                    logger.error(
                        "Notification failed: %s",
                        e
                    )



            # --------------------------------
            # Audit Logging
            # --------------------------------

            if AuditService:

                try:

                    AuditService.create_event(

                        event_type=
                        "ASSET_DISCOVERY_SCAN",

                        status=
                        "SUCCESS",

                        details={

                            "hostname":
                            asset.hostname,

                            "algorithm":
                            algorithm,

                            "risk":
                            asset.risk_level

                        }
                    )


                except Exception as e:

                    logger.error(
                        "Audit failed: %s",
                        e
                    )



            asset.scan_status = "SUCCESS"

            asset.last_scanned = (
                datetime.utcnow()
            )

            db.session.commit()


            return asset



        except Exception as e:


            logger.exception(
                "Asset discovery failed"
            )


            raise e



    # --------------------------------
    # Get Assets
    # --------------------------------

    @staticmethod
    def get_assets():

        return (
            DiscoveredAsset.query
            .order_by(
                DiscoveredAsset.created_at.desc()
            )
            .all()
        )



    # --------------------------------
    # Get Single Asset
    # --------------------------------

    @staticmethod
    def get_asset(asset_id):

        return (
            DiscoveredAsset.query
            .get_or_404(asset_id)
        )



    # --------------------------------
    # Delete Asset
    # --------------------------------

    @staticmethod
    def delete_asset(asset_id):

        asset = (
            DiscoveredAsset.query
            .get_or_404(asset_id)
        )

        db.session.delete(asset)

        db.session.commit()

        return True



    # --------------------------------
    # Rescan
    # --------------------------------

    @staticmethod
    def rescan(asset_id):

        asset = (
            DiscoveredAsset.query
            .get_or_404(asset_id)
        )


        return AssetDiscoveryService.scan_asset(
            asset.hostname,
            asset.port
        )
