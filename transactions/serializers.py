from rest_framework import serializers
from .models import Transaction, UserTransaction
from users.models import User


class UserTransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserTransaction
        fields = ['user', 'share']


class TransactionSerializer(serializers.ModelSerializer):
    senders = UserTransactionSerializer(many=True, write_only=True)
    receivers = UserTransactionSerializer(many=True, write_only=True)

    class Meta:
        model = Transaction
        fields = ['total_amount', 'senders', 'receivers', 'created_at']

    def create(self, validated_data):
        senders_data = validated_data.pop('senders')
        receivers_data = validated_data.pop('receivers')
        transaction = Transaction.objects.create(**validated_data)
        total_sender_share = sum([sender['share'] for sender in senders_data])
        total_receiver_share = sum([receiver['share'] for receiver in receivers_data])

        for sender_data in senders_data:
            user = sender_data['user']
            share = sender_data['share']

            # Calculate the amount the sender contributes
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

