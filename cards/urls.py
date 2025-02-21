# cards/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('issue-card/', views.issue_card_view, name='issue_card'),
    path('get-cards-by-account/', views.get_cards_by_account_view, name='get_cards_by_account'),
    path('update-card-status/', views.update_card_status_view, name='update_card_status'),
    path('set-spending-limit/', views.set_spending_limit_view, name='set_spending_limit'),
    path('get-card-balance/', views.get_card_balance_view, name='get_card_balance'),
    path('record-card-transaction/', views.record_card_transaction_view, name='record_card_transaction'),
    path('get-card-transaction-history/', views.get_card_transaction_history_view, name='get_card_transaction_history'),
]