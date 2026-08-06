# backend/app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# Database
db = SQLAlchemy()

# Database Migrations
migrate = Migrate()

# JWT Authentication
jwt = JWTManager()

# Cross-Origin Resource Sharing
cors = CORS()

# Serialization / Validation
ma = Marshmallow()

# API Rate Limiting
limiter = Limiter(
    key_func=get_remote_address
)
