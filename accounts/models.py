from django.db import models
from django.contrib.auth import get_user_model
import random

User = get_user_model()  # Reference Django's built-in User model

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(max_length=10, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Ensure account number is generated before saving."""
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_account_number():
        """Generate a unique 10-digit account number."""
        while True:
            account_number = ''.join(str(random.randint(0, 9)) for _ in range(10))
            if not Account.objects.filter(account_number=account_number).exists():
                return account_number

    def __str__(self):
        return f"Account {self.account_number} - {self.user.username}"
