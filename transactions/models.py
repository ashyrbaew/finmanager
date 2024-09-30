import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models
from users.models import User

class Transaction(models.Model):
    transaction_id = models.UUIDField(_('Transaction ID'), default=uuid.uuid4, editable=False, unique=True)
    total_amount = models.DecimalField(_('Total amount'), max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(_('Created date'), auto_now_add=True)

    def __str__(self):
        return str(self.transaction_id)


class UserTransaction(models.Model):
    ROLE_CHOICES = [
        ('sender', 'Sender'),
        ('receiver', 'Receiver'),
    ]

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='user_transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    role = models.CharField(_('Member role'), max_length=10, choices=ROLE_CHOICES)
    share = models.DecimalField(_('Transaction Share'), max_digits=10, decimal_places=2)
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.transaction.transaction_id}"
