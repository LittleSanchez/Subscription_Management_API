import uuid
from datetime import datetime, timezone

from app.db import db


class UserSubscription(db.Model):
    __tablename__ = "user_subscriptions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False, index=True
    )
    plan_id = db.Column(
        db.Integer, db.ForeignKey("subscription_plans.id"), nullable=False
    )

    start_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    end_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, index=True)

    user = db.relationship("User", backref=db.backref("subscriptions", lazy="dynamic"))
    plan = db.relationship(
        "SubscriptionPlan", backref=db.backref("subscriptions", lazy="dynamic")
    )

    def __repr__(self) -> str:
        return f"<Subscription user={self.user_id} plan={self.plan_id} active={self.is_active}>"
