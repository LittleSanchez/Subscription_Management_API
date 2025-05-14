from flask import Flask
from app.utils.token_blocklist import is_token_revoked
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from .db import db
from .routes import auth, plans, subscriptions


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql+psycopg2://postgres:frent123@localhost:5432/subscriptions"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]

    db.init_app(app)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_revoked(jwt_payload)

    Migrate(app, db)

    from app import models

    app.register_blueprint(auth.bp)
    app.register_blueprint(plans.bp)
    app.register_blueprint(subscriptions.bp)

    return app
