from flask import Blueprint
from flask_cors import CORS

admin_api = Blueprint("admin_api", __name__)
common_api = Blueprint("common_api", __name__)
user_api = Blueprint("user_api", __name__)

# TODO: SECURITY - CORS is wide open for development, needs to be limited for production
CORS(user_api)
CORS(common_api)
CORS(admin_api)
