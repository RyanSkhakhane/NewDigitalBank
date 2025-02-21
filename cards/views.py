# cards/views.py
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Card, CardTransaction
from accounts.models import Account
from .services import (issue_card, get_cards_by_account, update_card_status, set_spending_limit, get_card_balance, record_card_transaction, get_card_transaction_history,)

def issue_card_view(request):
    """API endpoint to issue a new card."""
    account_number = request.GET.get('account_number')
    card_type = request.GET.get('card_type')
    spending_limit = request.GET.get('spending_limit')

    card = issue_card(account_number, card_type, spending_limit)
    if card:
        return JsonResponse({"message": "Card issued successfully!", "card_number": card.card_number})
    return JsonResponse({"error": "Account not found."}, status=404)

def get_cards_by_account_view(request):
    """API endpoint to fetch all cards linked to an account."""
    account_number = request.GET.get('account_number')
    cards = get_cards_by_account(account_number)
    if cards:
        return JsonResponse({"cards": [{"card_number": card.card_number, "status": card.status} for card in cards]})
    return JsonResponse({"error": "Account not found."}, status=404)

def update_card_status_view(request):
    """API endpoint to block or activate a card."""
    card_number = request.GET.get('card_number')
    new_status = request.GET.get('new_status')

    card = update_card_status(card_number, new_status)
    if card:
        return JsonResponse({"message": f"Card status updated to {new_status}."})
    return JsonResponse({"error": "Card not found or invalid status."}, status=404)

def set_spending_limit_view(request):
    """API endpoint to set a spending limit on a card."""
    card_number = request.GET.get('card_number')
    limit = request.GET.get('limit')

    card = set_spending_limit(card_number, limit)
    if card:
        return JsonResponse({"message": f"Spending limit set to {limit}."})
    return JsonResponse({"error": "Card not found."}, status=404)

def get_card_balance_view(request):
    """API endpoint to fetch the balance of the account linked to the card."""
    card_number = request.GET.get('card_number')
    balance = get_card_balance(card_number)
    if balance is not None:
        return JsonResponse({"balance": balance})
    return JsonResponse({"error": "Card not found."}, status=404)

def record_card_transaction_view(request):
    """API endpoint to record a transaction made using a card."""
    card_number = request.GET.get('card_number')
    transaction_type = request.GET.get('transaction_type')
    amount = float(request.GET.get('amount'))
    merchant = request.GET.get('merchant')

    result = record_card_transaction(card_number, transaction_type, amount, merchant)
    if "successful" in result:
        return JsonResponse({"message": result})
    return JsonResponse({"error": result}, status=400)

def get_card_transaction_history_view(request):
    """API endpoint to fetch card transaction history."""
    card_number = request.GET.get('card_number')
    transactions = get_card_transaction_history(card_number)
    if transactions:
        return JsonResponse({"transactions": [
            {
                "transaction_type": t.transaction_type,
                "amount": t.amount,
                "merchant": t.merchant,
                "timestamp": t.timestamp
            } for t in transactions
        ]})
    return JsonResponse({"error": "Card not found."}, status=404)