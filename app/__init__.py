from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager

from app.routes.home_routes import home_bp
from app.routes.upload_routes import upload_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.download_routes import download_bp
from app.routes.auth_routes import auth_bp
from app.utils.directory_manager import create_directories
from app.database.db import engine, User, Base
from app.database.init_db import init_db


def create_app():

    app = Flask(__name__)
    app.secret_key = "lenovo-portal-secret-key-2024"

    CORS(
        app,
        resources={
            r"/*": {
                "origins": "*"
            }
        }
    )

    # ── Database ────────────────────────────────────────────────────────────
    # Ensure the users table exists and is populated from Excel on startup
    init_db()

    # ── Flask-Login ─────────────────────────────────────────────────────────
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please sign in to access that page."

    from sqlalchemy.orm import Session as DBSession

    @login_manager.user_loader
    def load_user(user_id):
        with DBSession(engine) as session:
            return session.get(User, user_id)

    # ── Directories ─────────────────────────────────────────────────────────
    create_directories()

    # ── Blueprints ──────────────────────────────────────────────────────────
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(download_bp)

    return app
