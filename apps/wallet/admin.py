"""
Admin configuration for Wallet app.
"""
from django.contrib import admin
from .models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Admin interface for Wallet model."""

    list_display = ['user', 'balance', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'user__phone_number']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Solde', {
            'fields': ('balance', 'is_active')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for Transaction model."""

    list_display = [
        'transaction_id',
        'wallet',
        'type',
        'amount',
        'status',
        'created_at'
    ]
    list_filter = ['type', 'status', 'created_at']
    search_fields = ['transaction_id', 'wallet__user__username', 'wave_transaction_id']
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']

    fieldsets = (
        ('Informations de base', {
            'fields': ('transaction_id', 'wallet', 'type', 'amount', 'status')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Wave API', {
            'fields': ('wave_transaction_id', 'wave_payment_url', 'metadata')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
