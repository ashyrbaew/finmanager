from django.test import TestCase
from users.models import User
from decimal import Decimal


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', balance=100.00)

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.balance, Decimal('100.00'))

    def test_update_balance(self):
        self.user.update_balance(Decimal('50.00'))
        self.assertEqual(self.user.balance, Decimal('150.00'))

        self.user.update_balance(Decimal('-25.00'))
        self.assertEqual(self.user.balance, Decimal('125.00'))

