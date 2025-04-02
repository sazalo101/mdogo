from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.payment_plan import PaymentPlan
from app import db

payment_plans_bp = Blueprint('payment_plans', __name__)

@payment_plans_bp.route('/search', methods=['GET'])
@jwt_required()
def search():
    query = request.args.get('query', '')
    results = db.payment_plans.find({
        "user_email": get_jwt_identity(),
        "$or": [
            {"item": {"$regex": query, "$options": "i"}},
            {"amount": {"$regex": str(query), "$options": "i"}}
        ]
    }).limit(10)
    
    return jsonify({
        "results": [dict(plan, **{"_id": str(plan["_id"]), "createdAt": plan["created_at"].isoformat()})
                   for plan in results]
    }), 200

@payment_plans_bp.route('/payment-plans', methods=['GET'])
@jwt_required()
def get_payment_plans():
    email = get_jwt_identity()
    plans = db.payment_plans.find({"user_email": email})
    return jsonify([PaymentPlan.from_dict(plan) | {"_id": str(plan["_id"])} for plan in plans]), 200

@payment_plans_bp.route('/payment-plan', methods=['POST'])
@jwt_required()
def add_payment_plan():
    email = get_jwt_identity()
    data = request.get_json()
    
    try:
        plan = PaymentPlan(
            user_email=email,
            item=data['item'],
            amount=data['amount'],
            installments=data['installments']
        )
        result = db.payment_plans.insert_one(plan.to_dict())
        return jsonify({"message": "Payment plan added", "id": str(result.inserted_id)}), 201
    except (KeyError, ValueError) as e:
        return jsonify({"message": "Invalid input data"}), 400