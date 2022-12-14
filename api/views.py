from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (
    WalletSerializer,
    TransactionsCreateSerializer,
    TransactionsListSerializer,
)

from transactions.models import Wallet, Transaction


class WalletsListCreate(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        user = self.request.user.id  # берем текущего юзера
        queryset = self.get_queryset().filter(user=user)
        serializer = WalletSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            if len(Wallet.objects.filter(user=request.user)) > 4:
                raise ValueError
        except ValueError:
            return Response("You cant create more than 5 wallets")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class WalletDetail(generics.RetrieveDestroyAPIView):
    lookup_field = "name"
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated,)


class TransactionsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user.id  # берем текущего юзера
        all_user_wallets = Wallet.objects.filter(user=user)
        queryset = Transaction.objects.filter(
            Q(sender__in=all_user_wallets) | Q(receiver__in=all_user_wallets)
        )  # фильтруем по текущему юзеру
        serializer = TransactionsListSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionsCreateSerializer(data=request.data)
        serializer.is_valid(
            raise_exception=True
        )  # проверка валидности данных согласно сериализатору
        try:
            # Проверку обьектов сделал тут иначе сериализатор не пропускает
            serializer.validated_data["sender"] = Wallet.objects.get(
                name=serializer.validated_data["sender"]
            )
            serializer.validated_data["receiver"] = Wallet.objects.get(
                name=serializer.validated_data["receiver"]
            )
            serializer.save()
        except ValueError:
            return Response(
                "Transactions are available only for wallets with the same currency"
            )
        except ObjectDoesNotExist:
            return Response("Sender or receiver does not exist")
        serializer = TransactionsCreateSerializer(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionDetail(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsListSerializer
    permission_classes = (IsAuthenticated,)


class TransactionsByWallet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        wallet = Wallet.objects.get(name=kwargs["name"])
        queryset = Transaction.objects.filter(
            Q(sender=wallet.id) | Q(receiver=wallet.id)
        )
        return Response(TransactionsListSerializer(queryset, many=True).data)


# class WalletListCreate(generics.ListCreateAPIView):
#     queryset = Wallet.objects.all()
#     serializer_class = WalletSerializer
#     # permission_classes = (IsAuthenticatedOrReadOnly,)
#
#     def list(self, request):
#         queryset = self.get_queryset().filter(
#             user=request.user
#         )  # фильтрация по авторизованному пользователю
#         serializer = WalletSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         try:
#             if len(Wallet.objects.filter(user=request.user)) > 4:
#                 raise ValueError
#         except ValueError:
#             return Response("You cant create more than 5 wallets")
#
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             serializer.data, status=status.HTTP_201_CREATED, headers=headers
#         )


# class TransactionList(generics.ListCreateAPIView):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly, )
#
#     def list(self, request):
#
#         user = self.request.user.id                 # берем текущего юзера
#         all_user_wallets = Wallet.objects.filter(user=user)
#         queryset = self.get_queryset()
#         print(queryset)
#         queryset = queryset.filter(Q(sender__in=all_user_wallets) | Q(receiver__in=all_user_wallets))   # фильтруем по текущему юзеру
#         serializer = TransactionSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:                                            # Проверка на равенство валюты и остальные проверки
#             self.perform_create(serializer)
#         except ValueError:
#             return Response('Transactions are available only for wallets with the same currency')
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
