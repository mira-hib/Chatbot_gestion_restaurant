"""
Wallet and Transaction models.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from apps.core.utils import generate_unique_id
from decimal import Decimal
from typing import Optional

User = get_user_model()


class Wallet(TimeStampedModel):
    """
    Wallet model for managing user balance.
    """
    user: models.OneToOneField = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wallet',
        verbose_name="Utilisateur"
    )

    balance: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Solde"
    )

    is_active: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    class Meta:
        verbose_name = "Portefeuille"
        verbose_name_plural = "Portefeuilles"

    def __str__(self) -> str:
        return f"Portefeuille de {self.user.username} - {self.formatted_balance}"

    @property
    def formatted_balance(self) -> str:
        """Return formatted balance."""
        return f"{self.balance:,.0f} FCFA"

    def can_deduct(self, amount: Decimal) -> bool:
        """Check if wallet has sufficient balance."""
        return self.balance >= amount

    def credit(self, amount: Decimal) -> None:
        """Add amount to wallet balance."""
        self.balance += amount
        self.save()

    def debit(self, amount: Decimal) -> None:
        """Deduct amount from wallet balance."""
        if not self.can_deduct(amount):
            from apps.core.exceptions import InsufficientBalanceException
            raise InsufficientBalanceException()

        self.balance -= amount
        self.save()


class Transaction(TimeStampedModel):
    """
    Transaction model for tracking wallet operations.
    """
    class Type(models.TextChoices):
        CREDIT = 'CREDIT', 'Crédit'
        DEBIT = 'DEBIT', 'Débit'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        COMPLETED = 'COMPLETED', 'Complétée'
        FAILED = 'FAILED', 'Échouée'
        CANCELLED = 'CANCELLED', 'Annulée'

    transaction_id: models.CharField = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        verbose_name="ID Transaction"
    )

    wallet: models.ForeignKey = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="Portefeuille"
    )

    type: models.CharField = models.CharField(
        max_length=10,
        choices=Type.choices,
        verbose_name="Type"
    )

    amount: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Montant"
    )

    status: models.CharField = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Statut"
    )

    description: models.TextField = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    # Wave API specific fields
    wave_transaction_id: models.CharField = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Wave Transaction ID"
    )

    wave_payment_url: models.URLField = models.URLField(
        blank=True,
        null=True,
        verbose_name="Wave Payment URL"
    )

    metadata: models.JSONField = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Métadonnées"
    )

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-created_at']

    def save(self, *args, **kwargs) -> None:
        """Generate transaction ID on creation."""
        if not self.transaction_id:
            prefix = "TXN-"
            self.transaction_id = generate_unique_id(prefix)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.transaction_id} - {self.type} - {self.amount} FCFA"

    @property
    def formatted_amount(self) -> str:
        """Return formatted amount."""
        return f"{self.amount:,.0f} FCFA"
