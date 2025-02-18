from django.db import models
from accounts.models import Account
from django.utils.timezone import now

class Transaction(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="sent_transactions")
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="received_transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.sender} → {self.receiver}: ${self.amount} at {self.timestamp}"
