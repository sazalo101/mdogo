import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Fixed MongoDB URI by using proper env variable retrieval
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://kimutaijaphet35:@Jkim_6699@cluster0.lsv8g2m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-very-secure-secret-key")
    SECRET_KEY = os.getenv("SECRET_KEY", "another-secure-key")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")