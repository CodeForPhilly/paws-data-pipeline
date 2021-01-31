import os

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = '1u9L#*&I3Ntc'
    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 Megs
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    from api.admin_api import admin_api
    from api.common_api import common_api
    app.register_blueprint(admin_api)
    app.register_blueprint(common_api)
    return app

if __name__ == "__main__":
    FLASK_PORT = os.getenv('FLASK_PORT', None)

    app = create_app()
    app.run(host='0.0.0.0', debug=True, port=FLASK_PORT)
