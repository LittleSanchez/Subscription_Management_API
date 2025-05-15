from flask import Blueprint, request, jsonify
from app.db import db
from app.models.subscription_plan import SubscriptionPlan

bp = Blueprint("plans", __name__, url_prefix="/plans")


@bp.route("/", methods=["POST"])
def create_plan():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    duration = data.get("duration_days")

    if not all([name, price, duration]):
        return jsonify({"message": "All fields are required"}), 400

    if SubscriptionPlan.query.filter_by(name=name).first():
        return jsonify({"message": "Plan already exists"}), 400

    plan = SubscriptionPlan(name=name, price=price, duration_days=duration)
    db.session.add(plan)
    db.session.commit()

    return jsonify({"message": "Plan created"}), 201


@bp.route("/", methods=["GET"])
def list_plans():
    plans = SubscriptionPlan.query.all()
    return jsonify(
        [
            {
                "id": plan.id,
                "name": plan.name,
                "price": str(plan.price),
                "duration_days": plan.duration_days,
            }
            for plan in plans
        ]
    )
