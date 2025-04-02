import sys
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# Ensure the models directory is in the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# This file marks the models directory as a Python package.
from models.intergration import Integration
from app import db

integrations_bp = Blueprint('integrations', __name__)

VALID_PLATFORMS = ['jiji', 'jumia', 'kilimall', 'alibaba', 'amazon']

@integrations_bp.route('/integrate/<platform>', methods=['POST'])
@jwt_required()
def integrate_marketplace(platform):
    email = get_jwt_identity()
    
    if platform not in VALID_PLATFORMS:
        return jsonify({"message": "Invalid platform"}), 400
    
    if db.integrations.find_one({"user_email": email, "platform": platform}):
        return jsonify({"message": f"Already integrated with {platform}"}), 400
    
    integration = Integration(email, platform)
    db.integrations.insert_one(integration.to_dict())
    return jsonify({"message": f"Successfully integrated with {platform}"}), 200

@integrations_bp.route('/integrations', methods=['GET'])
@jwt_required()
def get_integrations():
    email = get_jwt_identity()
    user_integrations = db.integrations.find({"user_email": email})
    return jsonify([Integration.from_dict(integration) | {"_id": str(integration["_id"])} 
                   for integration in user_integrations]), 200