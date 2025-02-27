from . import views
from django.urls import path

urlpatterns = [
    path('create/', views.create_account_view, name='create_account'),
    path('<int:account_number>/', views.get_account_view, name='get_account'),
    path('<int:account_number>/update/', views.update_balance_view, name='update_balance'),
    path('<int:account_number>/delete/', views.delete_account_view, name='delete_account'),
]