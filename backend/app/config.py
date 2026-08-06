# backend/app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Base configuration.
    """

    # Project Information
    PROJECT_NAME = "Quantum-Safe Cryptographic Infrastructure Platform"
    PROJECT_VERSION = "1.0.0"
    API_VERSION = "v1"

    # Security
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "development-jwt-secret-key"
    )

    # Database (Temporary for Phase 1)
    import os

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///instance/quantum_safe.db"
)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Settings
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """
    Development configuration.
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Testing configuration.
    """
    TESTING = True


class ProductionConfig(Config):
    """
    Production configuration.
    """
    DEBUG = False
