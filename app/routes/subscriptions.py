from flask import Blueprint, request, jsonify
from app.db import db
from app.models.user import User
from app.models.subscription_plan import SubscriptionPlan
from app.models.user_subscription import UserSubscription
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("subscriptions", __name__, url_prefix="/subscriptions")


@bp.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    email = data.get("email")
    plan_id = data.get("plan_id")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    plan = SubscriptionPlan.query.get(plan_id)
    if not plan:
        return jsonify({"message": "Plan not found"}), 404

    current = UserSubscription.query.filter_by(user_id=user.id, is_active=True).first()
    if current:
        current.is_active = False
        current.end_date = datetime.utcnow()

    new_subscription = UserSubscription(
        user_id=user.id,
        plan_id=plan.id,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=plan.duration_days),
        is_active=True,
    )
    db.session.add(new_subscription)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Subscription activated",
                "plan": plan.name,
                "ends_at": new_subscription.end_date.isoformat(),
            }
        ),
        201,
    )


@bp.route("/active", methods=["GET"])
@jwt_required()
def get_active_subscription():
    user_id = get_jwt_identity()

    subscription = (
        UserSubscription.query.filter_by(user_id=user_id, is_active=True)
        .join(SubscriptionPlan)
        .first()
    )

    if not subscription:
        return jsonify({"message": "No active subscription"}), 404

    return (
        jsonify(
            {
                "plan": subscription.plan.name,
                "price": str(subscription.plan.price),
                "started_at": subscription.start_date.isoformat(),
                "ends_at": subscription.end_date.isoformat(),
            }
        ),
        200,
    )


@bp.route("/cancel", methods=["POST"])
@jwt_required()
def cancel_subscription():
    user_id = get_jwt_identity()

    subscription = UserSubscription.query.filter_by(
        user_id=user_id, is_active=True
    ).first()

    if not subscription:
        return jsonify({"message": "No active subscription to cancel"}), 404

    subscription.is_active = False
    subscription.end_date = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "Subscription cancelled"}), 200
