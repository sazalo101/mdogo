from config import Config
from __init__ import create_app, db

app = create_app(Config)

if __name__ == '__main__':
    # Create indexes for performance
    db.users.create_index([("email", 1)], unique=True)
    db.payment_plans.create_index([("user_email", 1)])
    db.integrations.create_index([("user_email", 1), ("platform", 1)], unique=True)
    
    app.run(host='0.0.0.0', port=5000)