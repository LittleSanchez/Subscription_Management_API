from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from .db import db
# from .routes import auth, plans, subscriptions

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:frent123@localhost:5432/subscriptions'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'

    db.init_app(app)
    JWTManager(app)
    Migrate(app, db)
    
    from app import models

    # app.register_blueprint(auth.bp)
    # app.register_blueprint(plans.bp)
    # app.register_blueprint(subscriptions.bp)

    return app