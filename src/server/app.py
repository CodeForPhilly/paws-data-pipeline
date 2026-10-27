import math
import os
import time

import structlog
logger = structlog.get_logger()

from flask import Flask, jsonify

from flask_jwt_extended import JWTManager

try:   
    from secrets_dict import JWT_SECRET, APP_SECRET_KEY
except ImportError:   
    # Not running locally
    logger.info("Could not get secrets from file, trying environment **********")
    from os import environ

    try:
        JWT_SECRET = environ['JWT_SECRET']
        APP_SECRET_KEY = environ['APP_SECRET_KEY']   # not sure we use this any more, but just in case
    except KeyError:
        # Nor in environment
        # You're SOL for now
        logger.critical("Couldn't get secrets from file or environment")



# logger = structlog.get_logger()

# Send all Flask logs to structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.KeyValueRenderer(
            key_order=["event", "view", "peer"]
        ),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)



app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = JWT_SECRET  
app.config["JWT_MAX_TIMEOUT"] = 30*60 #Seconds

 # We'll use max for default but can be reduced for testing
app.config["JWT_ACCESS_TOKEN_EXPIRES"] =  app.config["JWT_MAX_TIMEOUT"] 

jwt = JWTManager(app)


app.secret_key = APP_SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500Mb
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

from api.admin_api import admin_api
from api.common_api import common_api
from api.user_api import user_api
from api.internal_api import internal_api
from api.api import limiter

limiter.init_app(app)


def _too_many_attempts_message(retry_after):
    """Tell the caller their attempts ran out and roughly how long to wait."""
    if not retry_after:
        return "Too many attempts. Please try again later."

    if retry_after < 60:
        amount, unit = retry_after, "second"
    else:
        amount, unit = math.ceil(retry_after / 60), "minute"  # round up (no 0 min)

    plural = "" if amount == 1 else "s"
    return f"Too many attempts. Please try again in about {amount} {unit}{plural}."


@app.errorhandler(429)
def rate_limit_exceeded(err):
    """Rate-limited callers get JSON like the rest of the API, not Flask's HTML page.

    Flask-Limiter already answers with 429 Too Many Requests, which is the right
    status; this only replaces the body so clients can tell "rate limited" apart
    from "bad credentials" instead of guessing from a non-200.
    """
    current_limit = limiter.current_limit
    retry_after = None
    if current_limit is not None:
        retry_after = max(1, int(current_limit.reset_at - time.time()))

    logger.info("Rate limit exceeded: %s, retry after %ss", err.description, retry_after)

    return (
        jsonify(
            {
                "error": "rate_limit_exceeded",
                "message": _too_many_attempts_message(retry_after),
                "retry_after": retry_after,
            }
        ),
        429,
    )


#  Emit a log entry at each level
app.register_blueprint(admin_api)
app.register_blueprint(common_api)
app.register_blueprint(user_api)
app.register_blueprint(internal_api)


# init_db_schema.start(connection)
logger.debug("Log sample - debug")        
logger.info("Log sample - info")    
logger.warn("Log sample - warn")
logger.error("Log sample - error")
logger.critical("Log sample - critical")

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", None)

    # create_app()
    app.run(host="0.0.0.0", debug=True, port=FLASK_PORT)
