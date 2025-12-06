"""
Serializers for Order models.
"""
from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from apps.menu.models import Product
from apps.core.exceptions import ProductUnavailableException
from typing import Dict, Any, List


class ProductDetailSerializer(serializers.Serializer):
    """
    Nested serializer for product details in OrderItem.
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.ImageField(required=False)


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    """
    product = ProductDetailSerializer(read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_image',
            'quantity',
            'unit_price',
            'subtotal',
        ]
        read_only_fields = ['id', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    formatted_total = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'user',
            'user_name',
            'status',
            'total_amount',
            'formatted_total',
            'delivery_address',
            'notes',
            'is_paid',
            'paid_at',
            'items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'order_number',
            'total_amount',
            'is_paid',
            'paid_at',
            'created_at',
            'updated_at'
        ]


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer for creating an order with items.
    """
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    delivery_address = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, items: List[Dict]) -> List[Dict]:
        """Validate order items."""
        if not items:
            raise serializers.ValidationError("Au moins un article est requis.")

        for item in items:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError(
                    "Chaque article doit avoir 'product_id' et 'quantity'."
                )

            try:
                product = Product.objects.get(id=item['product_id'])
                if not product.is_available:
                    raise ProductUnavailableException(
                        f"Le produit {product.name} n'est pas disponible."
                    )
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Produit avec l'ID {item['product_id']} introuvable."
                )

        return items

    @transaction.atomic
    def create(self, validated_data: Dict[str, Any]) -> Order:
        """Create order with items."""
        items_data: List[Dict] = validated_data.pop('items')
        user = self.context['request'].user

        # Create order
        order = Order.objects.create(
            user=user,
            delivery_address=validated_data.get('delivery_address', user.address),
            notes=validated_data.get('notes', ''),
        )

        # Create order items
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity']
            )

        # Calculate total
        order.calculate_total()
        order.save()

        return order

    def to_representation(self, instance: Order) -> Dict[str, Any]:
        """
        Return full order details with items.
        """
        return OrderSerializer(instance).data


class OrderStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating order status.
    """
    status = serializers.ChoiceField(choices=Order.Status.choices)
