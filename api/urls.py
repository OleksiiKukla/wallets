from django.urls import path, include, re_path

from .views import (
    WalletsListCreate,
    WalletDetail,
    TransactionsList,
    TransactionDetail,
    TransactionsByWallet,
)
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register('', WalletViewSet, basename='Wallet')

urlpatterns = [
    # path('', include(router.urls)),
    # path('<str:name>/', WalletViewSet.as_view({'get': 'list'})),
    path("transactions/", TransactionsList.as_view()),
    path("transactions/<int:pk>/", TransactionDetail.as_view()),
    path("transactions/<str:name>/", TransactionsByWallet.as_view()),
    path("", WalletsListCreate.as_view(), name="wallets"),
    path("<str:name>/", WalletDetail.as_view()),
]
