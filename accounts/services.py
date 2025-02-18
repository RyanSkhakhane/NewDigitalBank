from .models import Account

def create_account(user):
    """Create a new account for a user."""
    account = Account.objects.create(user=user)
    return account

def get_account(account_number):
    """Retrieve account details by account number."""
    return Account.objects.filter(account_number=account_number).first()

def update_balance(account_number, new_balance):
    """Update account balance."""
    account = get_account(account_number)
    if account:
        account.balance = new_balance
        account.save()
        return account
    return None

def delete_account(account_number):
    """Delete an account."""
    account = get_account(account_number)
    if account:
        account.delete()
        return True
    return False
