from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from .models import User, Session

def register_user(username, email, phone, password):
    """Register a new user."""
    try:
        user = User.objects.create_user(username=username, email=email, phone=phone, password=password)
        return {"success": True, "user_id": user.id}
    except IntegrityError:
        return {"success": False, "message": "Email or phone already exists."}

def login_user(email, password):
    """Authenticate user and create a session."""
    user = authenticate(email=email, password=password)
    if user:
        session = Session.objects.create(user=user)
        return {"success": True, "user_id": user.id, "session_id": session.id}
    return {"success": False, "message": "Invalid credentials"}

def logout_user(user_id):
    """Logout a user by deactivating their session."""
    Session.objects.filter(user_id=user_id, is_active=True).update(is_active=False)
    return {"success": True, "message": "Logout successful"}

def is_user_logged_in(user_id):
    """Check if user has an active session."""
    return Session.objects.filter(user_id=user_id, is_active=True).exists()


from .models import Account
from django.core.exceptions import ObjectDoesNotExist

def create_account(user_id, account_number):
    """Create a new bank account."""
    account = Account.objects.create(user_id=user_id, account_number=account_number)
    return {"success": True, "account_id": account.id}

def get_account(account_number):
    """Retrieve account details."""
    try:
        return Account.objects.get(account_number=account_number)
    except ObjectDoesNotExist:
        return None

def update_balance(account_number, amount):
    """Update account balance."""
    try:
        account = Account.objects.get(account_number=account_number)
        account.balance += amount
        account.save()
        return {"success": True, "new_balance": account.balance}
    except ObjectDoesNotExist:
        return {"success": False, "message": "Account not found."}

def delete_account(account_number):
    """Delete an account."""
    Account.objects.filter(account_number=account_number).delete()
    return {"success": True, "message": "Account deleted"}
