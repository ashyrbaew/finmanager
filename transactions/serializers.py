from django.db import transaction
from rest_framework import serializers

from users.models import User
from .models import Transaction, UserTransaction


class UserTransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserTransaction
        fields = ['user', 'share']

    def validate_share(self, value):
        if value <= 0:
            raise serializers.ValidationError("Share must be greater than zero.")
        return value


class TransactionSerializer(serializers.ModelSerializer):
    senders = UserTransactionSerializer(many=True, write_only=True)
    receivers = UserTransactionSerializer(many=True, write_only=True)

    class Meta:
        model = Transaction
        fields = ['total_amount', 'senders', 'receivers', 'created_at']

    def validate(self, data):
        if not data['senders'] or not data['receivers']:
            raise serializers.ValidationError("At least one sender and one receiver are required.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        senders_data = validated_data.pop('senders')
        receivers_data = validated_data.pop('receivers')

        total_sender_share = sum([sender['share'] for sender in senders_data])
        total_receiver_share = sum([receiver['share'] for receiver in receivers_data])

        if total_sender_share <= 0 or total_receiver_share <= 0:
            raise serializers.ValidationError("Total sender and receiver shares must be greater than zero.")

        transaction = Transaction.objects.create(**validated_data)

        for sender_data in senders_data:
            user = sender_data['user']
            share = sender_data['share']
            amount = (share / total_sender_share) * validated_data['total_amount']

            UserTransaction.objects.create(
                transaction=transaction,
                user=user,
                role='sender',
                share=share,
                amount=amount
            )

            user.update_balance(-amount)

        for receiver_data in receivers_data:
            user = receiver_data['user']
            share = receiver_data['share']
            amount = (share / total_receiver_share) * validated_data['total_amount']

            UserTransaction.objects.create(
                transaction=transaction,
                user=user,
                role='receiver',
                share=share,
                amount=amount
            )

            user.update_balance(amount)

        return transaction
