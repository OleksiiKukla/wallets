from django.core.exceptions import ObjectDoesNotExist

from decimal import Decimal

from rest_framework import serializers

from transactions.models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # можно прикрутить текущего юзера
    balance = serializers.HiddenField(default=Decimal(0))

    class Meta:
        model = Wallet
        fields = "__all__"


class TransactionsCreateSerializer(serializers.Serializer):
    sender = serializers.CharField(max_length=255)
    receiver = serializers.CharField(max_length=255)
    transfer_amount = serializers.DecimalField(max_digits=100, decimal_places=2)
    status = serializers.CharField(default="PAID")

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    # def create(self, validated_data):
    #      # Check the wallets exist
    #     sender = Wallet.objects.get(name=validated_data["sender"])
    #     receiver = Wallet.objects.get(name=validated_data["receiver"])
    #
    #
    #     return Transaction.objects.create(
    #         sender=sender,
    #         receiver=receiver,
    #         transfer_amount=validated_data["transfer_amount"],
    #     )


class TransactionsListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    sender = serializers.CharField(max_length=255)
    receiver = serializers.CharField(max_length=255)
    transfer_amount = serializers.DecimalField(max_digits=100, decimal_places=2)
    commision = serializers.DecimalField(max_digits=100, decimal_places=2)
    status = serializers.CharField(max_length=100, default="PAID")
    timestamp = serializers.DateTimeField()


# class TransactionSerializer(serializers.ModelSerializer):
#     # commision = serializers.HiddenField(default= Decimal(0))
#     status = serializers.CharField(default='PAID')
#     # sender_name = WalletSerializer(read_only=True)
#     class Meta:
#         model = Transaction
#         fields = "__all__"
