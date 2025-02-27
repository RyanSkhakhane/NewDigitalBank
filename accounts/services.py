from .models import Account
import logging

logger = logging.getLogger(__name__)

def create_account(user):
    """Create a new account for a user."""
    try:
        account = Account.objects.create(user=user)
        logger.info(f"Account created for user {user.id}")
        return account
    except Exception as e:
        logger.error(f"Error creating account for user {user.id}: {e}")
        return None

def get_account(account_number):
    """Retrieve account details by account number."""
    try:
        return Account.objects.filter(account_number=account_number).first()
    except Exception as e:
        logger.error(f"Error retrieving account {account_number}: {e}")
        return None

def update_balance(account_number, new_balance):
    """Update account balance."""
    if new_balance < 0:
        logger.error(f"Invalid balance {new_balance} for account {account_number}")
        return None
    account = get_account(account_number)
    if account:
        try:
            account.balance = new_balance
            account.save()
            logger.info(f"Updated balance for account {account_number} to {new_balance}")
            return account
        except Exception as e:
            logger.error(f"Error updating balance for account {account_number}: {e}")
            return None
    logger.error(f"Account {account_number} not found")
    return None

def delete_account(account_number):
    """Delete an account."""
    account = get_account(account_number)
    if account:
        try:
            account.delete()
            logger.info(f"Deleted account {account_number}")
            return True
        except Exception as e:
            logger.error(f"Error deleting account {account_number}: {e}")
            return False
    logger.error(f"Account {account_number} not found")
    return False
