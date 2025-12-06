"""
Core abstract models for the application.
"""
from django.db import models
from typing import Any


class TimeStampedModel(models.Model):
    """
    Abstract model with created_at and updated_at fields.
    """
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        verbose_name="Modifié le"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.__class__.__name__} - {self.pk}"
