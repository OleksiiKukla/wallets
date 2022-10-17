from decimal import Decimal

from django.db import models


from . import enums
from django.contrib.auth.models import User

from .utils import create_name, check_currency, check_balance


class Wallet(models.Model):

    name = models.CharField(max_length=8, null=True)
    type = models.CharField(max_length=25, choices=enums.Type_Cards_Choises.choices)
    currency = models.CharField(max_length=25, choices=enums.Currensy_Choises.choices)
    balance = models.DecimalField(max_digits=100, decimal_places=2)
    user = models.ForeignKey(
        User, verbose_name="User", on_delete=models.PROTECT, null=False
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = create_name()
        if self.currency == "RUB":
            self.balance += Decimal(100.00)
        else:
            self.balance += Decimal(3.00)
        super(Wallet, self).save(*args, **kwargs)


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, related_name="sender", on_delete=models.PROTECT)
    receiver = models.ForeignKey(
        Wallet, related_name="receiver", on_delete=models.PROTECT
    )
    transfer_amount = models.DecimalField(max_digits=100, decimal_places=2)
    commision = models.DecimalField(max_digits=100, decimal_places=2)
    status = models.CharField(max_length=100, default="PAID")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} {self.receiver.name} {self.transfer_amount} {self.commision} {self.status} {self.timestamp}"

    def save(self, *args, **kwargs):

        if not check_currency(self.sender.currency, self.receiver.currency):
            raise ValueError
        elif check_balance(self.sender.balance, self.transfer_amount):
            self.status = "FAILED - Not enough  money"

        if self.status == "PAID":

            if self.sender.user.id == self.receiver.user.id:
                self.commision = 0
            else:
                self.commision = self.transfer_amount * Decimal(0.10)

            self.sender.balance -= self.transfer_amount
            self.sender.save()

            self.transfer_amount -= self.commision

            self.receiver.balance += self.transfer_amount
            self.receiver.save()
        else:
            self.commision = Decimal(0)
        super(Transaction, self).save(*args, **kwargs)
