from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "account_number", "balance", "created_at")
    search_fields = ("account_number", "user__username")
