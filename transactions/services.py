from decimal import Decimal
from django.db.models import Sum


def calculate_user_balance(user):
    sent_total = (
        user.transactions.filter(
            role='sender'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    )

    received_total = (
        user.transactions.filter(
            role='receiver'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    )

    return received_total - sent_total
