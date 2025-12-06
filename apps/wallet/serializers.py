"""
Serializers for Wallet models.
"""
from rest_framework import serializers
from .models import Wallet, Transaction
from typing import Dict, Any


class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for Wallet model.
    """
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    formatted_balance = serializers.CharField(read_only=True)

    class Meta:
        model = Wallet
        fields = [
            'id',
            'user',
            'user_name',
            'balance',
            'formatted_balance',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'balance', 'created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction model.
    """
    wallet_user = serializers.CharField(source='wallet.user.full_name', read_only=True)
    formatted_amount = serializers.CharField(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'transaction_id',
            'wallet',
            'wallet_user',
            'type',
            'amount',
            'formatted_amount',
            'status',
            'description',
            'wave_transaction_id',
            'wave_payment_url',
            'metadata',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'transaction_id',
            'wave_transaction_id',
            'wave_payment_url',
            'created_at',
            'updated_at'
        ]


class RechargeRequestSerializer(serializers.Serializer):
    """
    Serializer for initiating a wallet recharge via Wave.
    """
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=100
    )
    phone_number = serializers.CharField(required=False)

    def validate_amount(self, value):
        """Validate minimum recharge amount."""
        if value < 100:
            raise serializers.ValidationError(
                "Le montant minimum de recharge est de 100 FCFA."
            )
        return value


class PayOrderSerializer(serializers.Serializer):
    """
    Serializer for paying an order from wallet.
    """
    order_id = serializers.IntegerField()
