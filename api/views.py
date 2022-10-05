from rest_framework import generics, status

from rest_framework.response import Response


from api.serializers import WalletSerializer, TransactionSerializer
from transactions.models import Wallet, Transaction


class WalletListCreate(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def list(self, request):
        queryset = self.get_queryset().filter(
            user=request.user
        )  # фильтрация по авторизованному пользователю
        serializer = WalletSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            if len(Wallet.objects.filter(user = request.user)) > 4:
                raise ValueError
        except ValueError:
            return Response('You cant create more than 5 wallets')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class WalletDetail(generics.RetrieveDestroyAPIView):
    lookup_field = "name"
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer



class TransactionListCreate(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def list(self, request):
        queryset = self.get_queryset().filter(
            user=request.user
        )  # фильтрация по авторизованному пользователю
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

     # def create(self, request, *args, **kwargs):
     #    serializer = self.get_serializer(data=request.data)
     #    serializer.is_valid(raise_exception=True)
     #    self.perform_create(serializer)
     #    headers = self.get_success_headers(serializer.data)
     #    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TransactionDetail(generics.RetrieveAPIView):
    lookup_field = "id"
    queryset = Transaction.objects.all()
    serializer_class = Transaction
