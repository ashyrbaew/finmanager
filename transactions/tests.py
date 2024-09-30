from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal
from users.models import User
from transactions.models import Transaction, UserTransaction


class TransactionAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.sender1 = User.objects.create(username='sender1', balance=1000.00)
        self.sender2 = User.objects.create(username='sender2', balance=2000.00)
        self.receiver1 = User.objects.create(username='receiver1', balance=0.00)
        self.receiver2 = User.objects.create(username='receiver2', balance=0.00)

        self.create_transaction_url = reverse('transactions-list')

    def test_create_transaction(self):
        data = {
            "total_amount": 1000,
            "senders": [
                {"user": self.sender1.id, "share": 1},
                {"user": self.sender2.id, "share": 4}
            ],
            "receivers": [
                {"user": self.receiver1.id, "share": 2},
                {"user": self.receiver2.id, "share": 3}
            ]
        }

        response = self.client.post(self.create_transaction_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check  balances
        self.sender1.refresh_from_db()
        self.sender2.refresh_from_db()
        self.receiver1.refresh_from_db()
        self.receiver2.refresh_from_db()

        # Sender shares should be 200 and 800 respectively
        self.assertEqual(self.sender1.balance, Decimal('800.00'))
        self.assertEqual(self.sender2.balance, Decimal('1200.00'))

        # Receiver shares should be 400 and 600 respectively
        self.assertEqual(self.receiver1.balance, Decimal('400.00'))
        self.assertEqual(self.receiver2.balance, Decimal('600.00'))

    def test_invalid_transaction_data(self):
        data = {
            "total_amount": 1000,
            "senders": [
                {"user": self.sender1.id}, # missing share inomation
                {"user": self.sender2.id, "share": 4}
            ],
            "receivers": [
                {"user": self.receiver1.id, "share": 2},
                {"user": self.receiver2.id, "share": 3}
            ]
        }

        response = self.client.post(self.create_transaction_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('share', response.data['senders'][0])

    def test_get_user_balance(self):
        get_balance_url = reverse('user-balance-detail', args=[self.receiver1.id])
        response = self.client.get(get_balance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], float(self.receiver1.balance))

