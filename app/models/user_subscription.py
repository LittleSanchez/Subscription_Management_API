from app.db import db
from datetime import datetime
import uuid

class UserSubscription(db.Model):
    __tablename__ = "user_subscriptions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("subscription_plans.id"), nullable=False)

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)

    is_active = db.Column(db.Boolean, default=True, index=True)

    user = db.relationship("User", backref=db.backref("subscriptions", lazy=True))
    plan = db.relationship("SubscriptionPlan", backref=db.backref("subscriptions", lazy=True))

    def __repr__(self):
        return f"<Subscription user={self.user_id} plan={self.plan_id} active={self.is_active}>"