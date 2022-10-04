from django.urls import path, include
from . import views
from .views import WalletListCreate, WalletDetail
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register('', WalletViewSet, basename='Wallet')

urlpatterns = [
    # path('', include(router.urls)),
    # path('<str:name>/', WalletViewSet.as_view({'get': 'list'})),
    path("<str:name>/", WalletDetail.as_view()),
    path("", WalletListCreate.as_view()),
]
