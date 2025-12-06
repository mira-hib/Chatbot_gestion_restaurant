"""
Admin configuration for Users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""

    list_display = [
        'username',
        'email',
        'phone_number',
        'telegram_username',
        'is_active',
        'created_at'
    ]
    list_filter = ['is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'phone_number', 'telegram_username']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations Telegram', {
            'fields': ('telegram_id', 'telegram_username')
        }),
        ('Informations supplémentaires', {
            'fields': ('phone_number', 'address')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('phone_number', 'telegram_id', 'telegram_username')
        }),
    )
