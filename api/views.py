from rest_framework import generics

from rest_framework.response import Response


from api.serializers import WalletSerializer
from transactions.models import Wallet


class WalletListCreate(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def list(self, request):
        queryset = self.get_queryset().filter(
            user=request.user
        )  # фильтрация по авторизованному пользователю
        serializer = WalletSerializer(queryset, many=True)
        return Response(serializer.data)


class WalletDetail(generics.RetrieveDestroyAPIView):
    lookup_field = "name"
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
