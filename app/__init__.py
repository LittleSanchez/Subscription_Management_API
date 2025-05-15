import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from app.db import db
from app.utils.token_blocklist import is_token_revoked
from app.routes import auth, plans, subscriptions

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///subscriptions.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]

    db.init_app(app)
    jwt = JWTManager(app)
    Migrate(app, db)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_revoked(jwt_payload)

    from app import models

    app.register_blueprint(auth.bp)
    app.register_blueprint(plans.bp)
    app.register_blueprint(subscriptions.bp)

    return app
