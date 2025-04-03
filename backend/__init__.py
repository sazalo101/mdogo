from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize Flask extensions
mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()
db = None

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Configure MongoDB directly rather than using URI
    # Flask-PyMongo configuration options
    app.config["MONGO_HOST"] = config_object.MONGO_HOST
    app.config["MONGO_PORT"] = config_object.MONGO_PORT
    app.config["MONGO_DBNAME"] = config_object.MONGO_DBNAME
    
    # Set auth params only if credentials are provided
    if config_object.MONGO_USERNAME and config_object.MONGO_PASSWORD:
        app.config["MONGO_USERNAME"] = config_object.MONGO_USERNAME
        app.config["MONGO_PASSWORD"] = config_object.MONGO_PASSWORD
    
    # Initialize extensions with app
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Set global db reference
    global db
    db = mongo.db
    
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