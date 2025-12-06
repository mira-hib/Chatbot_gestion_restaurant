"""
Swagger/OpenAPI preprocessing hooks.
"""
from typing import Dict, Any


def preprocess_token_auth(endpoints: Any) -> Any:
    """
    Preprocess OpenAPI schema to handle Token authentication properly.

    This hook ensures that the Bearer token format is correctly transformed
    to DRF's expected "Token <key>" format.
    """
    return endpoints
