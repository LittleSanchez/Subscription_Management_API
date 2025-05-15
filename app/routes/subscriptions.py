from datetime import datetime, timedelta, timezone

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from app.db import db
from app.models.user import User
from app.models.subscription_plan import SubscriptionPlan
from app.models.user_subscription import UserSubscription

bp = Blueprint("subscriptions", __name__, url_prefix="/subscriptions")


@bp.route("/subscribe", methods=["POST"])
@swag_from({
    "responses": {
        "201": {"description": "Subscription activated"},
        "400": {"description": "Missing email or plan_id"},
        "404": {"description": "User or plan not found"}
    }
})
def subscribe():
    data = request.get_json()
    email = data.get("email")
    plan_id = data.get("plan_id")

    if not email or not plan_id:
        return jsonify({"message": "Email and plan_id are required"}), 400

    user = User.query.filter_by(email=email.strip().lower()).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    plan = db.session.get(SubscriptionPlan, plan_id)
    if not plan:
        return jsonify({"message": "Plan not found"}), 404

    # Деактивація поточної активної підписки
    current = UserSubscription.query.filter_by(user_id=user.id, is_active=True).first()
    if current:
        current.is_active = False
        current.end_date = datetime.now(timezone.utc)

    # Створення нової підписки
    new_subscription = UserSubscription(
        user_id=user.id,
        plan_id=plan.id,
        start_date=datetime.now(timezone.utc),
        end_date=datetime.now(timezone.utc) + timedelta(days=plan.duration_days),
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
@swag_from({
    "responses": {
        "200": {"description": "Active subscription details"},
        "404": {"description": "No active subscription"},
        "401": {"description": "Unauthorized"}
    }
})
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
@swag_from({
    "responses": {
        "200": {"description": "Subscription cancelled"},
        "404": {"description": "No active subscription to cancel"},
        "401": {"description": "Unauthorized"}
    }
})
def cancel_subscription():
    user_id = get_jwt_identity()

    subscription = UserSubscription.query.filter_by(
        user_id=user_id, is_active=True
    ).first()

    if not subscription:
        return jsonify({"message": "No active subscription to cancel"}), 404

    subscription.is_active = False
    subscription.end_date = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({"message": "Subscription cancelled"}), 200
