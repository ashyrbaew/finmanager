from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, UserBalanceViewSet


router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'balances', UserBalanceViewSet, basename='user-balance')


urlpatterns = [
    path('', include(router.urls)),
]
