from django.contrib import admin
from .models import Wallet, Transaction


# Register your models here.


@admin.register(Wallet)
class walletAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "currency", "user", "created_on", "modified_on"]
