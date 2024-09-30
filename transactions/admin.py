from django.contrib import admin
from .models import Transaction, UserTransaction


class UserTransactionInline(admin.TabularInline):
    model = UserTransaction
    extra = 1


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'total_amount', 'created_at')
    search_fields = ('transaction_id',)
    inlines = [UserTransactionInline]


@admin.register(UserTransaction)
class UserTransactionAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'user__first_name', 'transaction', 'role', 'share', 'amount')
    list_filter = ('role',)
    search_fields = ('user__username', 'transaction__transaction_id')
