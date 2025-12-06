"""
Custom authentication classes.
"""
from rest_framework.authentication import TokenAuthentication
from typing import Optional, Tuple
from django.contrib.auth import get_user_model

User = get_user_model()


class BearerTokenAuthentication(TokenAuthentication):
    """
    Token authentication that accepts both 'Token' and 'Bearer' keywords.

    This allows Swagger UI (which uses Bearer) and other clients
    (which use Token) to work seamlessly.

    Examples:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        Authorization: Bearer 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    """
    keyword = ['Token', 'Bearer']

    def authenticate(self, request) -> Optional[Tuple[User, str]]:
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()

        if not auth or auth[0].lower() not in ['token', 'bearer']:
            return None

        if len(auth) == 1:
            return None
        elif len(auth) > 2:
            return None

        # Get the token
        token_key = auth[1]

        return self.authenticate_credentials(token_key)
