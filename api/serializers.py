from decimal import Decimal

from rest_framework import serializers

from transactions.models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Wallet
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    commision = serializers.HiddenField(default= Decimal(0))
    status = serializers.CharField(default='PAID')
    class Meta:
        model = Transaction
        fields = "__all__"



