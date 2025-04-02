from datetime import datetime

class Integration:
    def __init__(self, user_email, platform):
        self.user_email = user_email
        self.platform = platform
        self.status = "active"
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "user_email": self.user_email,
            "platform": self.platform,
            "status": self.status,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        return {
            "platform": data["platform"],
            "status": data["status"],
            "createdAt": data["created_at"].isoformat() if isinstance(data["created_at"], datetime) else data["created_at"]
        }