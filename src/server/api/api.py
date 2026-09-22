from flask import Blueprint
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

admin_api = Blueprint("admin_api", __name__)
common_api = Blueprint("common_api", __name__)
user_api = Blueprint("user_api", __name__)
internal_api = Blueprint("internal_api", __name__)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    strategy="fixed-window",
    headers_enabled=True  # Send Retry-After / X-RateLimit-* on every response
)


# TODO: SECURITY - CORS is wide open for development, needs to be limited for production
CORS(user_api)
CORS(common_api)
CORS(admin_api)
