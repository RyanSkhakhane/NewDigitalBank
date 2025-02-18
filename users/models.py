from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):
    """Custom User model extending Django's built-in authentication system."""
    phone = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.username  # or self.email

class Session(models.Model):
    """Tracks user login sessions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Session for {self.user.username} at {self.login_time}"


class Account(models.Model):
    """Represents a user's bank account."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"
