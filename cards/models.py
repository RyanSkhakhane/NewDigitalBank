from django.db import models
from accounts.models import Account
import random
from datetime import datetime, timedelta

class Card(models.Model):
    CARD_TYPES = [("Debit", "Debit"), ("Credit", "Credit")]
    STATUS_CHOICES = [("Active", "Active"), ("Blocked", "Blocked")]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="cards")
    card_number = models.CharField(max_length=16, unique=True)
    card_type = models.CharField(max_length=10, choices=CARD_TYPES)
    cvv = models.CharField(max_length=3)
    expiry_date = models.CharField(max_length=5)  # MM/YY format
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")
    spending_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Ensure card number, CVV, and expiry date are generated before saving."""
        if not self.card_number:
            self.card_number = self.generate_card_number()
        if not self.cvv:
            self.cvv = self.generate_cvv()
        if not self.expiry_date:
            self.expiry_date = self.generate_expiry_date()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_card_number():
        """Generate a unique 16-digit card number."""
        while True:
            card_number = ''.join(str(random.randint(0, 9)) for _ in range(16))
            if not Card.objects.filter(card_number=card_number).exists():
                return card_number

    @staticmethod
    def generate_cvv():
        """Generate a 3-digit CVV."""
        return str(random.randint(100, 999))

    @staticmethod
    def generate_expiry_date():
        """Generate an expiry date (3 years from now)."""
        expiry = datetime.now() + timedelta(days=3 * 365)
        return expiry.strftime("%m/%y")

    def __str__(self):
        return f"{self.card_type} Card {self.card_number} - {self.account}"


class CardTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("Purchase", "Purchase"),
        ("Withdrawal", "Withdrawal"),
        ("Refund", "Refund"),
    ]

    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    merchant = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.timestamp}"
