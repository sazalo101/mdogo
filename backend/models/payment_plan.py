from datetime import datetime

class PaymentPlan:
    def __init__(self, user_email, item, amount, installments):
        self.user_email = user_email
        self.item = item
        self.amount = float(amount)
        self.installments = int(installments)
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "user_email": self.user_email,
            "item": self.item,
            "amount": self.amount,
            "installments": self.installments,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        return {
            "item": data["item"],
            "amount": data["amount"],
            "installments": data["installments"],
            "createdAt": data["created_at"].isoformat()
        }