from .models import Card, CardTransaction
from accounts.models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

def issue_card(account_number, card_type, spending_limit=None):
    """Issue a new card for an account."""
    try:
        account = Account.objects.get(account_number=account_number)
        card = Card.objects.create(account=account, card_type=card_type, spending_limit=spending_limit)
        return card
    except ObjectDoesNotExist:
        return None

def get_cards_by_account(account_number):
    """Fetch all cards linked to an account."""
    try:
        account = Account.objects.get(account_number=account_number)
        return account.cards.all()
    except ObjectDoesNotExist:
        return []

def update_card_status(card_number, new_status):
    """Block or activate a card."""
    if new_status not in ["Active", "Blocked"]:
        return None

    try:
        card = Card.objects.get(card_number=card_number)
        card.status = new_status
        card.save()
        return card
    except ObjectDoesNotExist:
        return None

def set_spending_limit(card_number, limit):
    """Set a spending limit on a card."""
    try:
        card = Card.objects.get(card_number=card_number)
        card.spending_limit = limit
        card.save()
        return card
    except ObjectDoesNotExist:
        return None

def get_card_balance(card_number):
    """Fetch the balance of the account linked to the card."""
    try:
        card = Card.objects.get(card_number=card_number)
        return card.account.balance
    except ObjectDoesNotExist:
        return None

@transaction.atomic
def record_card_transaction(card_number, transaction_type, amount, merchant=None):
    """Record a transaction made using a card."""
    try:
        card = Card.objects.get(card_number=card_number)
        account = card.account

        if card.spending_limit and amount > card.spending_limit:
            return "Transaction declined: Spending limit exceeded."

        if account.balance < amount:
            return "Transaction declined: Insufficient funds."

        # Deduct from balance
        account.balance -= amount
        account.save()

        # Record the transaction
        CardTransaction.objects.create(
            card=card, transaction_type=transaction_type, amount=amount, merchant=merchant
        )
        return f"Transaction successful! New Account Balance: {account.balance}"
    except ObjectDoesNotExist:
        return "Card not found."

def get_card_transaction_history(card_number):
    """Fetch card transaction history."""
    try:
        card = Card.objects.get(card_number=card_number)
        return card.transactions.order_by("-timestamp")
    except ObjectDoesNotExist:
        return []
