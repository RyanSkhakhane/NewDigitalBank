from django.db import transaction
from .models import Transaction
from accounts.models import Account
from django.core.exceptions import ObjectDoesNotExist

@transaction.atomic
def create_transaction(sender_account_number, receiver_account_number, amount):
    """Process a transaction between two accounts."""
    try:
        sender = Account.objects.get(account_number=sender_account_number)
        receiver = Account.objects.get(account_number=receiver_account_number)

        if sender.balance < amount:
            return "Insufficient funds!"

        # Deduct from sender
        sender.balance -= amount
        sender.save()

        # Add to receiver
        receiver.balance += amount
        receiver.save()

        # Record transaction
        txn = Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)
        return f"Transaction successful! New sender balance: {sender.balance}"

    except ObjectDoesNotExist:
        return "One or both accounts do not exist."

def get_transaction_history(account_number):
    """Retrieve transaction history for an account."""
    try:
        account = Account.objects.get(account_number=account_number)
        transactions = Transaction.objects.filter(sender=account) | Transaction.objects.filter(receiver=account)
        return transactions.order_by("-timestamp")
    except ObjectDoesNotExist:
        return []
