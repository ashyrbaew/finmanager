import uuid

from django.db import models
from users.models import User


class Transaction(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class UserTransaction(models.Model):
    ROLE_CHOICES = [
        ('sender', 'Sender'),
        ('receiver', 'Receiver'),
    ]

    transaction = models.ForeignKey(Transaction, related_name='user_transactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    share = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.transaction.transaction_id}"
