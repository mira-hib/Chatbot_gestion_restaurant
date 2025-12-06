"""
Admin configuration for Menu app.
"""
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""

    list_display = ['name', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""

    list_display = [
        'name',
        'category',
        'price',
        'is_available',
        'preparation_time',
        'order'
    ]
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['category', 'order', 'name']
    list_editable = ['price', 'is_available', 'order']

    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'description', 'category')
        }),
        ('Prix et disponibilité', {
            'fields': ('price', 'is_available', 'preparation_time')
        }),
        ('Média', {
            'fields': ('image',)
        }),
        ('Ordre', {
            'fields': ('order',)
        }),
    )
