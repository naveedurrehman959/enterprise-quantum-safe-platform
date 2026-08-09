"""
Asset Discovery Business Orchestration Layer

Workflow:

Request
    ↓
DNS Resolver
    ↓
TLS Scanner
    ↓
Certificate Parser
    ↓
Discovered Asset Database
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

from app.algorithm_inventory.services import (
    AlgorithmInventoryService
)

from app.risk_assessment.services import (
    RiskAssessmentService
)

from app.policy_engine.services import (
    PolicyEngineService
)


logger = logging.getLogger(__name__)


class AssetDiscoveryService:

    # ==========================================================
    # Scan Asset
    # ==========================================================

    @staticmethod
    def scan_asset(target: str, port: int = 443):

        asset = None

        try:

            logger.info(
                "Starting asset discovery for %s:%s",
                target,
                port
            )

            # ==================================================
            # 1. DNS Resolution
            # ==================================================

            host = DNSResolver.resolve(target)

            if not host:
                raise ValueError(
                    f"DNS resolution failed for {target}"
                )

            hostname = host.get("hostname")
            ip_address = host.get("ip_address")

            logger.info(
                "DNS resolved %s -> %s",
                hostname,
                ip_address
            )

            # ==================================================
            # 2. TLS Scan
            # ==================================================

            scan = TLSScanner.scan(
                hostname=hostname,
                ip_address=ip_address,
                port=port
            )

            if not scan:
                raise ValueError(
                    f"TLS scan returned no result for {target}"
                )

            # ==================================================
            # 3. Certificate Parsing
            # ==================================================

            certificate_der = scan.get(
                "certificate_der"
            )

            if not certificate_der:
                raise ValueError(
                    f"No TLS certificate returned for {target}"
                )

            cert = CertificateParser.parse(
                certificate_der
            )

            if not cert:
                raise ValueError(
                    f"Certificate parsing failed for {target}"
                )

            # ==================================================
            # 4. Extract Algorithm
            # ==================================================

            algorithm = cert.get(
                "public_key_algorithm"
            )

            if algorithm:

                algorithm = str(
                    algorithm
                ).strip().upper()

            else:

                algorithm = None

            logger.info(
                "Certificate algorithm for %s: %s",
                hostname,
                algorithm
            )

            # ==================================================
            # 5. Find Existing Asset
            # ==================================================

            asset = DiscoveredAsset.query.filter_by(
                hostname=hostname,
                port=port
            ).first()

            if asset:

                logger.info(
                    "Updating existing discovered asset: %s:%s",
                    hostname,
                    port
                )

            else:

                logger.info(
                    "Creating new discovered asset: %s:%s",
                    hostname,
                    port
                )

                asset = DiscoveredAsset()

            # ==================================================
            # 6. Update Discovered Asset
            # ==================================================

            asset.hostname = hostname

            asset.ip_address = ip_address

            asset.port = port

            asset.tls_version = scan.get(
                "tls_version"
            )

            asset.cipher_suite = scan.get(
                "cipher_suite"
            )

            asset.public_key_algorithm = algorithm

            asset.key_size = cert.get(
                "key_size"
            )

            asset.signature_algorithm = cert.get(
                "signature_algorithm"
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

            asset.fingerprint_sha256 = cert.get(
                "fingerprint_sha256"
            )

            asset.valid_from = cert.get(
                "valid_from"
            )

            asset.valid_to = cert.get(
                "valid_to"
            )

            asset.scan_status = "RUNNING"

            asset.scan_error = None

            asset.last_scanned = datetime.utcnow()

            db.session.add(asset)

            db.session.commit()

            logger.info(
                "Discovered asset saved successfully. ID=%s",
                asset.id
            )

            # ==================================================
            # 7. Algorithm Inventory
            # ==================================================

            if not algorithm:

                logger.warning(
                    "Certificate algorithm unavailable for %s",
                    hostname
                )

                asset.risk_level = "UNKNOWN"
                asset.risk_score = 50
                asset.policy_decision = "MANUAL_REVIEW"
                asset.migration_required = True

            else:

                try:

                    logger.info(
                        "Registering algorithm in inventory: %s",
                        algorithm
                    )

                    inventory_result = (
                        AlgorithmInventoryService
                        .auto_register_algorithm(
                            algorithm_name=algorithm,
                            key_size=asset.key_size
                        )
                    )

                    logger.info(
                        "Algorithm inventory result: %s",
                        inventory_result
                    )

                except Exception as inventory_error:

                    logger.exception(
                        "Algorithm inventory registration failed "
                        "for %s",
                        algorithm
                    )

                    raise RuntimeError(
                        "Algorithm inventory registration failed: "
                        f"{inventory_error}"
                    ) from inventory_error

                # ==================================================
                # 8. Risk Assessment
                # ==================================================

                try:

                    risk = (
                        RiskAssessmentService
                        .assess_algorithm(
                            algorithm
                        )
                    )

                    asset.risk_level = risk.get(
                        "risk_level",
                        "UNKNOWN"
                    )

                    asset.risk_score = risk.get(
                        "risk_score",
                        0
                    )

                    asset.recommended_algorithm = (
                        risk.get(
                            "recommended_algorithm"
                        )
                    )

                    logger.info(
                        "Risk assessment: %s -> %s (%s)",
                        algorithm,
                        asset.risk_level,
                        asset.risk_score
                    )

                except Exception as risk_error:

                    logger.exception(
                        "Risk assessment failed for %s",
                        algorithm
                    )

                    asset.risk_level = "UNKNOWN"
                    asset.risk_score = 50

                    raise RuntimeError(
                        "Risk assessment failed: "
                        f"{risk_error}"
                    ) from risk_error

                # ==================================================
                # 9. Policy Engine
                # ==================================================

                try:

                    policy = (
                        PolicyEngineService
                        .evaluate_policy(
                            algorithm
                        )
                    )

                    asset.policy_decision = policy.get(
                        "decision",
                        "MANUAL_REVIEW"
                    )

                    asset.migration_required = (
                        asset.policy_decision
                        in [
                            "BLOCK",
                            "MIGRATION_REQUIRED",
                            "HYBRID_REQUIRED"
                        ]
                    )

                    if not asset.recommended_algorithm:

                        asset.recommended_algorithm = (
                            policy.get(
                                "recommended_algorithm"
                            )
                        )

                    logger.info(
                        "Policy decision: %s -> %s",
                        algorithm,
                        asset.policy_decision
                    )

                except Exception as policy_error:

                    logger.exception(
                        "Policy evaluation failed for %s",
                        algorithm
                    )

                    asset.policy_decision = (
                        "MANUAL_REVIEW"
                    )

                    asset.migration_required = True

            # ==================================================
            # 10. Final Asset State
            # ==================================================

            asset.scan_status = "SUCCESS"

            asset.last_scanned = datetime.utcnow()

            db.session.commit()

            logger.info(
                "Asset discovery completed successfully: %s",
                hostname
            )

            return asset

        except Exception as error:

            logger.exception(
                "Asset discovery failed for %s:%s",
                target,
                port
            )

            db.session.rollback()

            # If an asset was already created, record failure.
            if asset:

                try:

                    asset.scan_status = "FAILED"

                    asset.scan_error = str(
                        error
                    )

                    asset.last_scanned = (
                        datetime.utcnow()
                    )

                    db.session.add(asset)

                    db.session.commit()

                except Exception:

                    db.session.rollback()

            raise

    # ==========================================================
    # Get All Assets
    # ==========================================================

    @staticmethod
    def get_assets():

        return (
            DiscoveredAsset.query
            .order_by(
                DiscoveredAsset.created_at.desc()
            )
            .all()
        )

    # ==========================================================
    # Get Single Asset
    # ==========================================================

    @staticmethod
    def get_asset(asset_id):

        return (
            DiscoveredAsset.query
            .get_or_404(asset_id)
        )

    # ==========================================================
    # Delete Asset
    # ==========================================================

    @staticmethod
    def delete_asset(asset_id):

        asset = (
            DiscoveredAsset.query
            .get_or_404(asset_id)
        )

        db.session.delete(asset)

        db.session.commit()

        return True

    # ==========================================================
    # Rescan Asset
    # ==========================================================

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
