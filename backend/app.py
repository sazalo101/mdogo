from flask import Flask, Blueprint
from config import Config
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from roots.auth import auth_bp
from roots.payment_plans import payment_plans_bp

integrations_bp = Blueprint('integrations', __name__)

@integrations_bp.route('/integrations', methods=['GET'])
def get_integrations():
    return {"message": "Integrations endpoint"}

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(payment_plans_bp, url_prefix='/api')
app.register_blueprint(integrations_bp, url_prefix='/api')

# Global MongoDB collections
db = mongo.db

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {"message": "Resource not found"}, 404

@app.errorhandler(500)
def server_error(error):
    return {"message": "Internal server error"}, 500

if __name__ == '__main__':
    # Create indexes for performance
    db.users.create_index([("email", 1)], unique=True)
    db.payment_plans.create_index([("user_email", 1)])
    db.integrations.create_index([("user_email", 1), ("platform", 1)], unique=True)
    
    app.run(host='0.0.0.0', port=5000)

# This file marks the routes directory as a Python package.