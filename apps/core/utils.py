"""
Utility functions for the application.
"""
from typing import Dict, Any, Optional
from decimal import Decimal
import uuid


def generate_unique_id(prefix: str = "") -> str:
    """
    Generate a unique ID with optional prefix.

    Args:
        prefix: String prefix for the ID

    Returns:
        Unique string ID
    """
    unique_id: str = str(uuid.uuid4().hex[:12])
    return f"{prefix}{unique_id}" if prefix else unique_id


def format_money(amount: Decimal, currency: str = "FCFA") -> str:
    """
    Format money amount with currency.

    Args:
        amount: Decimal amount
        currency: Currency code

    Returns:
        Formatted string
    """
    return f"{amount:,.0f} {currency}"


def calculate_percentage(amount: Decimal, percentage: int) -> Decimal:
    """
    Calculate percentage of an amount.

    Args:
        amount: Base amount
        percentage: Percentage value

    Returns:
        Calculated amount
    """
    return (amount * Decimal(percentage)) / Decimal(100)


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format (basic validation).

    Args:
        phone: Phone number string

    Returns:
        True if valid, False otherwise
    """
    cleaned: str = phone.replace(" ", "").replace("-", "").replace("+", "")
    return cleaned.isdigit() and len(cleaned) >= 9
