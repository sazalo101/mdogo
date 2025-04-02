from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from __init__ import db, bcrypt 

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    if db.users.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    user = User(email, password, bcrypt)
    db.users.insert_one(user.to_dict())
    token = create_access_token(identity=email)
    return jsonify({"token": token}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = db.users.find_one({"email": email})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=email)
    return jsonify({"token": token}), 200

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    email = get_jwt_identity()
    user = db.users.find_one({"email": email}, {"_id": 0, "password": 0})
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(User.from_dict(user)), 200