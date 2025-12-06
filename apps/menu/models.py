"""
Menu and Product models.
"""
from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel
from decimal import Decimal
from typing import Optional


class Category(TimeStampedModel):
    """
    Product category model.
    """
    name: models.CharField = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom"
    )

    description: models.TextField = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    is_active: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )

    order: models.IntegerField = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['order', 'name']

    def __str__(self) -> str:
        return self.name


class Product(TimeStampedModel):
    """
    Product/Dish model.
    """
    name: models.CharField = models.CharField(
        max_length=200,
        verbose_name="Nom"
    )

    description: models.TextField = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    category: models.ForeignKey = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Catégorie"
    )

    price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Prix"
    )

    image: models.ImageField = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name="Image"
    )

    is_available: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="Disponible"
    )

    preparation_time: models.IntegerField = models.IntegerField(
        default=15,
        help_text="Temps de préparation en minutes",
        verbose_name="Temps de préparation"
    )

    order: models.IntegerField = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['category', 'order', 'name']

    def __str__(self) -> str:
        return f"{self.name} - {self.price} FCFA"

    @property
    def formatted_price(self) -> str:
        """Return formatted price."""
        return f"{self.price:,.0f} FCFA"
