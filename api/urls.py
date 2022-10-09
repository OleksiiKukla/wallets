from django.urls import path, include, re_path
from . import views
from .views import WalletListCreate, WalletDetail, TransactionListCreate, TransactionDetail, TransactionsByWallet
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register('', WalletViewSet, basename='Wallet')

urlpatterns = [
    # path('', include(router.urls)),
    # path('<str:name>/', WalletViewSet.as_view({'get': 'list'})),
    path("transaction/", TransactionListCreate.as_view()),
    path("transaction/<int:pk>/", TransactionDetail.as_view()),
    path("transaction/<str:name>/", TransactionsByWallet.as_view()),

    path("", WalletListCreate.as_view()),
    path("<str:name>/", WalletDetail.as_view()),

    path("login/", include('rest_framework.urls')),
    path('registration/auth/', include('djoser.urls')), # регистрация /auth/users/
    re_path(r'^auth/', include('djoser.urls.authtoken')),# Авторизация по токенам auth/token/login

]
