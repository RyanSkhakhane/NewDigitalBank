from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "amount", "timestamp")
    search_fields = ("sender__account_number", "receiver__account_number")
