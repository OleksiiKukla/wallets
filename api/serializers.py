from rest_framework import serializers

from transactions.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Wallet
        fields = "__all__"
