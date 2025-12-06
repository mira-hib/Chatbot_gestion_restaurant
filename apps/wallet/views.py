"""
Views for Wallet and Transaction management.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone
from .models import Wallet, Transaction
from .serializers import (
    WalletSerializer,
    TransactionSerializer,
    RechargeRequestSerializer,
    PayOrderSerializer
)
from .wave_service import WaveService
from apps.orders.models import Order
from apps.core.exceptions import InsufficientBalanceException
from typing import Any


class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Wallet operations.
    """
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return wallet for current user or all for staff."""
        if self.request.user.is_staff:
            return Wallet.objects.select_related('user')
        return Wallet.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_wallet(self, request) -> Response:
        """Get current user's wallet."""
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(wallet)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def recharge(self, request) -> Response:
        """
        Initiate wallet recharge via Wave.
        """
        serializer = RechargeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        phone_number = serializer.validated_data.get(
            'phone_number',
            request.user.phone_number
        )

        # Get or create wallet
        wallet, created = Wallet.objects.get_or_create(user=request.user)

        # Create pending transaction
        txn = Transaction.objects.create(
            wallet=wallet,
            type=Transaction.Type.CREDIT,
            amount=amount,
            status=Transaction.Status.PENDING,
            description=f"Recharge de {amount} FCFA via Wave"
        )

        # Initiate Wave payment
        try:
            wave_service = WaveService()
            wave_response = wave_service.initiate_payment(
                amount=amount,
                phone_number=phone_number,
                transaction_id=txn.transaction_id
            )

            # Update transaction with Wave details
            txn.wave_transaction_id = wave_response.get('wave_transaction_id')
            txn.wave_payment_url = wave_response.get('payment_url')
            txn.metadata = wave_response
            txn.save()

            return Response(
                {
                    'message': 'Paiement initié avec succès',
                    'transaction': TransactionSerializer(txn).data,
                    'payment_url': txn.wave_payment_url,
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            txn.status = Transaction.Status.FAILED
            txn.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def recharge_fictif(self, request) -> Response:
        """
        Rechargement fictif du portefeuille (pour tests/démo).
        Crédite directement le wallet sans passer par Wave.
        """
        serializer = RechargeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']

        # Get or create wallet
        wallet, created = Wallet.objects.get_or_create(user=request.user)

        # Crédit direct du wallet
        with transaction.atomic():
            wallet.credit(amount)

            # Create completed transaction
            txn = Transaction.objects.create(
                wallet=wallet,
                type=Transaction.Type.CREDIT,
                amount=amount,
                status=Transaction.Status.COMPLETED,
                description=f"Rechargement fictif de {amount} FCFA"
            )

        return Response(
            {
                'message': 'Rechargement effectué avec succès',
                'transaction': TransactionSerializer(txn).data,
                'new_balance': wallet.formatted_balance
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def pay_order(self, request) -> Response:
        """
        Pay for an order using wallet balance.
        """
        serializer = PayOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Commande introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )

        if order.is_paid:
            return Response(
                {'error': 'Cette commande est déjà payée'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get wallet
        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return Response(
                {'error': 'Portefeuille introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check balance
        if not wallet.can_deduct(order.total_amount):
            raise InsufficientBalanceException(
                f"Solde insuffisant. Votre solde: {wallet.formatted_balance}, "
                f"Montant requis: {order.formatted_total}"
            )

        # Process payment
        with transaction.atomic():
            # Debit wallet
            wallet.debit(order.total_amount)

            # Create transaction record
            txn = Transaction.objects.create(
                wallet=wallet,
                type=Transaction.Type.DEBIT,
                amount=order.total_amount,
                status=Transaction.Status.COMPLETED,
                description=f"Paiement commande {order.order_number}",
                metadata={'order_id': order.id}
            )

            # Update order
            order.is_paid = True
            order.paid_at = timezone.now()
            order.status = Order.Status.CONFIRMED
            order.save()

        return Response(
            {
                'message': 'Paiement effectué avec succès',
                'transaction': TransactionSerializer(txn).data,
                'order_number': order.order_number,
                'remaining_balance': wallet.formatted_balance
            },
            status=status.HTTP_200_OK
        )


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Transaction history.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return transactions for current user or all for staff."""
        if self.request.user.is_staff:
            return Transaction.objects.select_related('wallet__user')

        try:
            wallet = Wallet.objects.get(user=self.request.user)
            return Transaction.objects.filter(wallet=wallet)
        except Wallet.DoesNotExist:
            return Transaction.objects.none()

    @action(detail=False, methods=['get'])
    def my_transactions(self, request) -> Response:
        """Get current user's transaction history."""
        transactions = self.get_queryset()
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
