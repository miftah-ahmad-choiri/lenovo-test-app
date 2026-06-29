from flask import Flask
from flask_cors import CORS

from app.routes.home_routes import home_bp
from app.routes.upload_routes import upload_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.download_routes import download_bp
from app.utils.directory_manager import create_directories


def create_app():

    app = Flask(__name__)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": "*"
            }
        }
    )

    # Create required folders
    create_directories()

    # Register Blueprint
    app.register_blueprint(home_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(download_bp)

    return app