"""
Admin configuration for Orders app.
"""
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem."""
    model = OrderItem
    extra = 0
    readonly_fields = ['unit_price', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""

    list_display = [
        'order_number',
        'user',
        'status',
        'total_amount',
        'is_paid',
        'created_at'
    ]
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__phone_number']
    readonly_fields = ['order_number', 'total_amount', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    fieldsets = (
        ('Informations de base', {
            'fields': ('order_number', 'user', 'status')
        }),
        ('Montant', {
            'fields': ('total_amount', 'is_paid', 'paid_at')
        }),
        ('Livraison', {
            'fields': ('delivery_address', 'notes')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        """Recalculate total on save."""
        super().save_model(request, obj, form, change)
        obj.calculate_total()
        obj.save()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model."""

    list_display = ['order', 'product', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['created_at']
    search_fields = ['order__order_number', 'product__name']
    readonly_fields = ['unit_price', 'subtotal']
