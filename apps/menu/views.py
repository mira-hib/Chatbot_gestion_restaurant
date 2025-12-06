"""
Views for Menu management.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Prefetch
from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductListSerializer,
    MenuSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category CRUD operations.
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

    def get_permissions(self):
        """Allow anyone to view, but require auth for modifications."""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product CRUD operations.
    """
    queryset = Product.objects.select_related('category').filter(is_available=True)
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_permissions(self):
        """Allow anyone to view, but require auth for modifications."""
        if self.action in ['list', 'retrieve', 'by_category']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def by_category(self, request) -> Response:
        """Get products grouped by category."""
        category_id = request.query_params.get('category_id')

        if category_id:
            products = self.queryset.filter(category_id=category_id)
        else:
            products = self.queryset.all()

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def menu(self, request) -> Response:
        """
        Get complete menu with categories and products.
        Optimized for n8n/Telegram bot consumption.
        """
        categories = Category.objects.filter(
            is_active=True
        ).prefetch_related(
            Prefetch(
                'products',
                queryset=Product.objects.filter(is_available=True)
            )
        )

        menu_data = []
        for category in categories:
            category_data = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'products': ProductListSerializer(
                    category.products.all(),
                    many=True
                ).data
            }
            menu_data.append(category_data)

        return Response({
            'menu': menu_data,
            'total_categories': len(menu_data),
            'total_products': sum(len(cat['products']) for cat in menu_data)
        })
