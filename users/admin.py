from django.contrib import admin
from .models import User, Account, Session

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Session)
