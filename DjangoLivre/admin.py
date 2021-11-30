from django.contrib import admin
from .models import Client, Account, Transfer


admin.site.register(Account)
admin.site.register(Client)
admin.site.register(Transfer)
