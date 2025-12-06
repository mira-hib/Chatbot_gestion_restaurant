"""
Custom exceptions for the application.
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class InsufficientBalanceException(APIException):
    """Raised when user has insufficient balance."""
    status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail: str = "Solde insuffisant pour effectuer cette opération."
    default_code: str = "insufficient_balance"


class InvalidOrderStateException(APIException):
    """Raised when order state transition is invalid."""
    status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail: str = "État de commande invalide pour cette opération."
    default_code: str = "invalid_order_state"


class ProductUnavailableException(APIException):
    """Raised when product is not available."""
    status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail: str = "Ce produit n'est pas disponible."
    default_code: str = "product_unavailable"


class PaymentFailedException(APIException):
    """Raised when payment fails."""
    status_code: int = status.HTTP_402_PAYMENT_REQUIRED
    default_detail: str = "Le paiement a échoué."
    default_code: str = "payment_failed"


class WaveAPIException(APIException):
    """Raised when Wave API returns an error."""
    status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail: str = "Erreur lors de la communication avec Wave."
    default_code: str = "wave_api_error"
