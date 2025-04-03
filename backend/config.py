import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Add MongoDB URI configuration
    MONGO_URI = f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:{os.getenv('MONGO_PORT', '27017')}/{os.getenv('MONGO_DBNAME', 'mdogopay')}"
    
    # Keep existing config parameters
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secure-jwt-secret-key-change-in-production")
    SECRET_KEY = os.getenv("SECRET_KEY", "another-secure-key-change-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")