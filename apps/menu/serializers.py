"""
Serializers for Menu models.
"""
from rest_framework import serializers
from .models import Category, Product
from typing import Dict, Any


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'is_active',
            'order',
            'products_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_products_count(self, obj: Category) -> int:
        """Return count of available products in category."""
        return obj.products.filter(is_available=True).count()


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    formatted_price = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'category',
            'category_name',
            'price',
            'formatted_price',
            'image',
            'is_available',
            'preparation_time',
            'order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for product lists.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category_name',
            'price',
            'is_available',
            'image',
        ]


class MenuSerializer(serializers.Serializer):
    """
    Serializer for complete menu (categories with products).
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    products = ProductListSerializer(many=True, read_only=True)
