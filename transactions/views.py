from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from .models import Transaction, UserTransaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Transaction failed: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserBalanceViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        return Response({
            'user_id': user.id,
            'balance': float(user.balance)
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def balance_history(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date or not end_date:
            return Response({'error': 'Please provide both start_date and end_date'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            if start_date > end_date:
                return Response({'error': 'End date must be later than start date'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        transactions = UserTransaction.objects.filter(
            user=user,
            transaction__created_at__range=[start_date, end_date]
        )

        total_amount = sum(
            transaction.amount if transaction.role == 'receiver' else -transaction.amount
            for transaction in transactions
        )

        return Response({
            'user_id': user.id,
            'balance_change': float(total_amount),
            'balance': float(user.balance + total_amount)
        }, status=status.HTTP_200_OK)
