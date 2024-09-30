from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    balance = models.DecimalField(_('Net balance'), max_digits=12, decimal_places=2, default=0.00)
    photo = models.ImageField(_('Profile image'), upload_to='photos/', blank=True, null=True)
    phone_number = models.CharField(_('Phone'), max_length=15, blank=True, null=True)
    address = models.TextField(_('Address'), blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        verbose_name="groups",
        related_name='custom_user_set',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        verbose_name="user permissions",
        related_name='custom_user_permissions_set',
    )

    def update_balance(self, amount):
        #tO avoid race conditions
        User.objects.filter(id=self.id).update(balance=F('balance') + amount)
        self.refresh_from_db()

    def __str__(self):
        return f"{self.username} - {self.first_name}"