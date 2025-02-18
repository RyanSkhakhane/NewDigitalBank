from django.contrib import admin
from .models import Card, CardTransaction

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("account", "card_number", "card_type", "status", "expiry_date", "spending_limit")
    search_fields = ("card_number", "account__account_number")

@admin.register(CardTransaction)
class CardTransactionAdmin(admin.ModelAdmin):
    list_display = ("card", "transaction_type", "amount", "merchant", "timestamp")
    search_fields = ("card__card_number",)