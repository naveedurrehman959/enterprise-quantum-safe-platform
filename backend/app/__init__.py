# backend/app/__init__.py

from flask import Flask, jsonify

from .config import DevelopmentConfig
from .extensions import (
    db,
    migrate,
    jwt,
    cors,
    ma,
    limiter,
)

from .models.token_blocklist import TokenBlocklist


def create_app():

    app = Flask(__name__)

    # ---------------------------------
    # Load Configuration
    # ---------------------------------

    app.config.from_object(DevelopmentConfig)

    # ---------------------------------
    # Initialize Extensions
    # ---------------------------------

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)

    # ---------------------------------
    # Import JWT Callbacks
    # ---------------------------------

    from app.auth import jwt_callbacks

    # ---------------------------------
    # Register Authentication Blueprint
    # ---------------------------------

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.profile.routes import profile_bp
    app.register_blueprint(profile_bp)
    # ---------------------------------
    # Register Crypto Blueprint
    # ---------------------------------

    from app.crypto.routes import crypto_bp
    app.register_blueprint(crypto_bp)

    # ---------------------------------
    # Register PKI Blueprint
    # ---------------------------------
        # ---------------------------------
    # Register Search Blueprint
    # ---------------------------------

    from app.search.routes import search_bp

    app.register_blueprint(search_bp)
        # ---------------------------------
    # Register Reports Blueprint
    # ---------------------------------

    from app.reports.routes import reports_bp

    app.register_blueprint(reports_bp)
        # ---------------------------------
    # Register Notifications Blueprint
    # ---------------------------------

    from app.notifications.routes import notifications_bp

    app.register_blueprint(notifications_bp)

    from app.pki.routes import pki_bp
    app.register_blueprint(pki_bp)

    # ---------------------------------
    # Register Vault Blueprint
    # ---------------------------------

    from app.vault.routes import vault_bp
    app.register_blueprint(vault_bp)

    # ---------------------------------
    # Register Compliance Blueprint
    # ---------------------------------

    from app.compliance.routes import compliance_bp
    app.register_blueprint(compliance_bp)

    # ---------------------------------
    # Register Crypto Agility Blueprint
    # ---------------------------------

    from app.crypto_agility.routes import crypto_agility_bp
    app.register_blueprint(crypto_agility_bp)

    # ---------------------------------
    # Register Monitoring Blueprint
    # ---------------------------------
    from app.settings.routes import settings_bp

    app.register_blueprint(settings_bp)
    # ---------------------------------
    # Register Monitoring Blueprint
    # ---------------------------------

    from app.monitoring.routes import monitoring_bp
    app.register_blueprint(
        monitoring_bp
    )

    # ---------------------------------
    # Register Algorithm Inventory Blueprint
    # ---------------------------------

    from app.algorithm_inventory.routes import inventory_bp
    app.register_blueprint(
        inventory_bp,
        url_prefix="/api/v1/inventory"
    )

    # ---------------------------------
    # Register Risk Assessment Blueprint
    # ---------------------------------

    from app.risk_assessment.routes import risk_bp
    app.register_blueprint(risk_bp)
     
    # ---------------------------------
    # Register Policy Engine Blueprint
    # ---------------------------------

    from app.policy_engine.routes import policy_bp
    app.register_blueprint(
        policy_bp,
        url_prefix="/api/v1/policy"
    )
    from app.metrics.routes import metrics_bp

    app.register_blueprint(
        metrics_bp
    )
    # ---------------------------------
    # Register Migration Engine Blueprint
    # ---------------------------------

    from app.migration_engine.routes import migration_bp
    app.register_blueprint(migration_bp)


    from app.audit.routes import audit_bp
    app.register_blueprint(audit_bp)
    
    from app.dashboard.routes import dashboard_bp
    app.register_blueprint(dashboard_bp)
    # ---------------------------------
    # Register Session Management Blueprint
    # ---------------------------------

    from app.session_management.routes import session_bp
    app.register_blueprint(
        session_bp,
        url_prefix="/api/v1"
    )

    # ---------------------------------
    # Rate Limit Error Handler
    # ---------------------------------

    @app.errorhandler(429)
    def ratelimit_handler(e):

        return jsonify(
            {
                "error": "Too many requests.",
                "message": str(e.description),
            }
        ), 429

    # ---------------------------------
    # JWT Token Revocation Callback
    # ---------------------------------

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):

        jti = jwt_payload["jti"]

        token = (
            db.session.query(TokenBlocklist.id)
            .filter_by(jti=jti)
            .scalar()
        )

        return token is not None

    # ---------------------------------
    # Health Check Endpoint
    # ---------------------------------

    @app.route("/health", methods=["GET"])
    def health_check():

        return jsonify(
            {
                "status": "healthy",
                "service": app.config["PROJECT_NAME"],
                "version": app.config["PROJECT_VERSION"],
            }
        ), 200

    return app
