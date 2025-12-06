"""
Views for Order management.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Order, OrderItem
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer
)
from apps.core.exceptions import InvalidOrderStateException
from typing import Any


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order CRUD operations.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return orders for current user or all for staff."""
        if self.request.user.is_staff:
            return Order.objects.select_related('user').prefetch_related('items__product')
        return Order.objects.filter(
            user=self.request.user
        ).select_related('user').prefetch_related('items__product')

    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None) -> Response:
        """Confirm an order."""
        order: Order = self.get_object()

        if order.status != Order.Status.PENDING:
            raise InvalidOrderStateException(
                "Seules les commandes en attente peuvent être confirmées."
            )

        order.status = Order.Status.CONFIRMED
        order.save()

        return Response(
            {
                'message': 'Commande confirmée avec succès',
                'order': OrderSerializer(order).data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None) -> Response:
        """Cancel an order."""
        order: Order = self.get_object()

        if order.status in [Order.Status.DELIVERED, Order.Status.CANCELLED]:
            raise InvalidOrderStateException(
                "Cette commande ne peut pas être annulée."
            )

        order.status = Order.Status.CANCELLED
        order.save()

        return Response(
            {
                'message': 'Commande annulée avec succès',
                'order': OrderSerializer(order).data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None) -> Response:
        """Update order status (staff only)."""
        if not request.user.is_staff:
            return Response(
                {'error': 'Autorisation requise'},
                status=status.HTTP_403_FORBIDDEN
            )

        order: Order = self.get_object()
        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order.status = serializer.validated_data['status']
        order.save()

        return Response(
            {
                'message': 'Statut mis à jour avec succès',
                'order': OrderSerializer(order).data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def my_orders(self, request) -> Response:
        """Get current user's orders."""
        orders = Order.objects.filter(
            user=request.user
        ).select_related('user').prefetch_related('items__product')

        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request) -> Response:
        """Get pending orders (staff only)."""
        if not request.user.is_staff:
            return Response(
                {'error': 'Autorisation requise'},
                status=status.HTTP_403_FORBIDDEN
            )

        orders = Order.objects.filter(
            status=Order.Status.PENDING
        ).select_related('user').prefetch_related('items__product')

        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
