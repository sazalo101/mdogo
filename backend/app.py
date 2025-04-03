from config import Config
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# Initialize Flask app and extensions
app = Flask(__name__)
app.config.from_object(Config)
mongo = PyMongo(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Get the db reference from mongo
db = mongo.db

if __name__ == '__main__':
    # Ensure indexes are created
    db.users.create_index([("email", 1)], unique=True)
    db.payment_plans.create_index([("user_email", 1)])
    db.integrations.create_index([("user_email", 1), ("platform", 1)], unique=True)
    
    app.run(host='0.0.0.0', port=5000)