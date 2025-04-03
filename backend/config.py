import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use MongoDB connection parameters instead of URI
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
    MONGO_DBNAME = os.getenv("MONGO_DBNAME", "mdogopay")
    MONGO_USERNAME = os.getenv("MONGO_USERNAME", "")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")
    
    # Keep other configuration parameters
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secure-jwt-secret-key-change-in-production")
    SECRET_KEY = os.getenv("SECRET_KEY", "another-secure-key-change-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")