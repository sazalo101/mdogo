from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize Flask extensions
bcrypt = Bcrypt()
jwt = JWTManager()
db = None
mongo_client = None

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Initialize MongoDB client directly with pymongo
    global mongo_client, db
    
    # Connect to MongoDB directly
    mongo_client = MongoClient(
        host=config_object.MONGO_HOST, 
        port=config_object.MONGO_PORT,
        username=config_object.MONGO_USERNAME if config_object.MONGO_USERNAME else None,
        password=config_object.MONGO_PASSWORD if config_object.MONGO_PASSWORD else None
    )
    
    # Get database reference
    db = mongo_client[config_object.MONGO_DBNAME]
    
    # Initialize other extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Import and register blueprints
    from roots.auth import auth_bp
    from roots.payment_plans import payment_plans_bp
    from roots.integration import integrations_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(payment_plans_bp, url_prefix='/api')
    app.register_blueprint(integrations_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"message": "Resource not found"}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {"message": "Internal server error"}, 500
    
    return app