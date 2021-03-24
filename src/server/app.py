import os

from flask import Flask

from flask_jwt_extended import JWTManager

from secrets import JWT_SECRET, APP_SECRET_KEY

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = JWT_SECRET
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 300  # Seconds for timeout. 60 for testing.
jwt = JWTManager(app)


app.secret_key = APP_SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500 Megs
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
from api.admin_api import admin_api
from api.common_api import common_api
from api.user_api import user_api

app.register_blueprint(admin_api)
app.register_blueprint(common_api)
app.register_blueprint(user_api)

app.logger.setLevel('INFO')  # By default, Docker appears to set at INFO but VSCode at WARNING 


# init_db_schema.start(connection)


if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", None)

    # create_app()
    app.run(host="0.0.0.0", debug=True, port=FLASK_PORT)
