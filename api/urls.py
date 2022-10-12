from django.urls import path, include, re_path

from .views import (
    WalletListCreate,
    WalletDetail,
    TransactionList,
    TransactionDetail,
    TransactionsByWallet,
)
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register('', WalletViewSet, basename='Wallet')

urlpatterns = [
    # path('', include(router.urls)),
    # path('<str:name>/', WalletViewSet.as_view({'get': 'list'})),
    path("transactions/", TransactionList.as_view()),
    path("transactions/<int:pk>/", TransactionDetail.as_view()),
    path("transactions/<str:name>/", TransactionsByWallet.as_view()),
    path("", WalletListCreate.as_view(), name="wallets"),
    path("<str:name>/", WalletDetail.as_view()),
    # path("login/", include("rest_framework.urls")),
    # path("registration/auth/", include("djoser.urls")),  # регистрация /auth/users/
    # re_path(
    #     r"^auth/", include("djoser.urls.authtoken")
    # ),  # Авторизация по токенам auth/token/login
]
