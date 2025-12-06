"""
User models for authentication and profile management.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import TimeStampedModel
from typing import Optional


class User(AbstractUser, TimeStampedModel):
    """
    Custom User model extending Django's AbstractUser.
    """
    telegram_id: models.BigIntegerField = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="ID Telegram"
    )

    telegram_username: models.CharField = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Nom d'utilisateur Telegram"
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format: '+221771234567'"
    )
    phone_number: models.CharField = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        verbose_name="Numéro de téléphone"
    )

    address: models.TextField = models.TextField(
        blank=True,
        verbose_name="Adresse de livraison"
    )

    is_active: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.username} ({self.phone_number})"

    @property
    def full_name(self) -> str:
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def has_telegram(self) -> bool:
        """Check if user has Telegram linked."""
        return self.telegram_id is not None
