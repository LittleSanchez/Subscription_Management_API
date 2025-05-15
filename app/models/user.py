import uuid
from datetime import datetime, timezone

from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates

from app.db import db
from app.utils.validators import validate_password


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    is_active = db.Column(db.Boolean, default=False)
    is_staff = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def set_password(self, password: str) -> None:
        validate_password(password)
        self.password_hash = generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @validates("email")
    def validate_email(self, _, value: str) -> str:
        assert "@" in value, "Email must contain @"
        return value.strip().lower()
