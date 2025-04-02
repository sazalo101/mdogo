from datetime import datetime

class User:
    def __init__(self, email, password, bcrypt):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        return {
            "email": data["email"],
            "createdAt": data["created_at"].isoformat() if isinstance(data["created_at"], datetime) else data["created_at"]
        }