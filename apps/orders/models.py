"""
Order and OrderItem models.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from apps.core.utils import generate_unique_id
from apps.menu.models import Product
from decimal import Decimal
from typing import Optional

User = get_user_model()


class Order(TimeStampedModel):
    """
    Order model representing a customer order.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmée'
        PREPARING = 'PREPARING', 'En préparation'
        READY = 'READY', 'Prête'
        DELIVERED = 'DELIVERED', 'Livrée'
        CANCELLED = 'CANCELLED', 'Annulée'

    order_number: models.CharField = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name="Numéro de commande"
    )

    user: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Client"
    )

    status: models.CharField = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Statut"
    )

    total_amount: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Montant total"
    )

    delivery_address: models.TextField = models.TextField(
        blank=True,
        verbose_name="Adresse de livraison"
    )

    notes: models.TextField = models.TextField(
        blank=True,
        verbose_name="Notes"
    )

    is_paid: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name="Payée"
    )

    paid_at: models.DateTimeField = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Payée le"
    )

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']

    def save(self, *args, **kwargs) -> None:
        """Generate order number on creation."""
        if not self.order_number:
            self.order_number = generate_unique_id("CMD-")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.order_number} - {self.user.username}"

    def calculate_total(self) -> Decimal:
        """Calculate total amount from order items."""
        total: Decimal = sum(
            item.subtotal for item in self.items.all()
        )
        self.total_amount = total
        return total

    @property
    def formatted_total(self) -> str:
        """Return formatted total amount."""
        return f"{self.total_amount:,.0f} FCFA"


class OrderItem(TimeStampedModel):
    """
    OrderItem model representing a product in an order.
    """
    order: models.ForeignKey = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Commande"
    )

    product: models.ForeignKey = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Produit"
    )

    quantity: models.IntegerField = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Quantité"
    )

    unit_price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Prix unitaire"
    )

    subtotal: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Sous-total"
    )

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def save(self, *args, **kwargs) -> None:
        """Calculate subtotal before saving."""
        self.unit_price = self.product.price
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product.name} x{self.quantity}"
