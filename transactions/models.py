from decimal import Decimal

from django.db import models
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


from . import enums
from django.contrib.auth.models import User

from .utils import create_name, check_currency, check_balance, check_owner_wallet


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
        return f"{self.user}--{self.name} -- {self.currency} --{self.balance}"

    def save(self, *args, **kwargs):
        if not self.name:
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

    sender = models.ForeignKey(Wallet, related_name="sender", on_delete=models.PROTECT)
    receiver = models.ForeignKey(
        Wallet, related_name="receiver", on_delete=models.PROTECT
    )
    transer_amount = models.DecimalField(max_digits=100, decimal_places=2)
    commision = models.DecimalField(max_digits=100, decimal_places=2)
    status = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} {self.receiver.name} {self.transer_amount} {self.commision} {self.status} {self.timestamp}"

    def save(self, *args, **kwargs):
        # Сделать проверку на наличие кошельков
        sender = Wallet.objects.get(id=self.sender.id)
        receiver = Wallet.objects.get(id=self.receiver.id)

        if not check_currency(sender.currency, receiver.currency):
            raise ValueError
        elif check_balance(sender.balance, self.transer_amount):
            self.status = 'FAILED - Not enough  money'

        # Сделать проверку на статус, если фейлед выход ?

        if sender.user.id == receiver.user.id:
            self.commision = 0
        else:
            self.commision = self.transer_amount * Decimal(0.10)

        sender.balance -= self.transer_amount
        sender.save()

        self.transer_amount -= self.commision

        receiver.balance += self.transer_amount
        receiver.save()

        super(Transaction, self).save(*args, **kwargs)


