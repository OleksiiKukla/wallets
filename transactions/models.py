from decimal import Decimal

from django.db import models


from . import enums
from django.contrib.auth.models import User

from .utils import create_name


class Wallet(models.Model):

    name = models.CharField(max_length=8, null=True)
    type = models.CharField(max_length=25, choices=enums.Type_Cards_Choises.choices)
    currency = models.CharField(max_length=25, choices=enums.Currensy_Choises.choices)
    balance = models.DecimalField(max_digits=100, decimal_places=2)
    user = models.ForeignKey(
        User, verbose_name="User", on_delete=models.PROTECT, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} {self.name} {self.type} {self.user} {self.balance} {self.created_on}"

    def save(self, *args, **kwargs):
        self.name = create_name()
        if self.currency == "RUB":
            self.balance += Decimal(100.00)
        else:
            self.balance += Decimal(3.00)
        super(Wallet, self).save(*args, **kwargs)


class Transaction(models.Model):
    """
    Transaction entity
    - sender - wallet_id
    - receiver - wallet_id
    - transer_amount of money that “sender” send to “receiver”. Example - 5.00
    - commision - 0.00 if no commision else transfer_amount * 0.10
    - status - PAID if no problems else FAILED
    - timestamp - datetime when transaction was created
    """

    sender = models.ForeignKey(Wallet, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        Wallet, related_name="receiver", on_delete=models.CASCADE
    )
    transer_amount = models.DecimalField(max_digits=100, decimal_places=2)
    commision = models.IntegerField()
    status = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now=True)
