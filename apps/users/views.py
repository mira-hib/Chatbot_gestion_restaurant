"""
Views for User authentication and management.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from typing import Any
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    LoginOrRegisterSerializer,
    LoginPasswordSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User CRUD operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        """Return appropriate permissions."""
        if self.action in ['create', 'login_or_register', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login_or_register(self, request) -> Response:
        """
        Login or register user via Telegram.
        Creates a new user if telegram_id doesn't exist.
        """
        serializer = LoginOrRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        telegram_id: int = serializer.validated_data['telegram_id']
        phone_number: str = serializer.validated_data.get('phone_number', '')

        # Try to find existing user
        user: User = User.objects.filter(telegram_id=telegram_id).first()

        if not user:
            # Create new user
            user = User.objects.create(
                username=f"user_{telegram_id}",
                telegram_id=telegram_id,
                telegram_username=serializer.validated_data.get('telegram_username', ''),
                phone_number=phone_number,
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', ''),
            )
            user.set_unusable_password()
            user.save()

            # Create token for new user
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    'message': 'Compte créé avec succès',
                    'user': UserSerializer(user).data,
                    'token': token.key,
                    'is_new': True
                },
                status=status.HTTP_201_CREATED
            )

        # Get or create token for existing user
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'message': 'Connexion réussie',
                'user': UserSerializer(user).data,
                'token': token.key,
                'is_new': False
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request) -> Response:
        """
        Login with username/email and password.
        Returns user data and authentication token.
        """
        serializer = LoginPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Get or create token
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'message': 'Connexion réussie',
                'user': UserSerializer(user).data,
                'token': token.key
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def me(self, request) -> Response:
        """Get current user information."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
