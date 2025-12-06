"""
Serializers for User models.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from typing import Dict, Any

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    full_name = serializers.CharField(read_only=True)
    has_telegram = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'telegram_id',
            'telegram_username',
            'has_telegram',
            'address',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'phone_number',
            'telegram_id',
            'telegram_username',
            'address',
        ]

    def create(self, validated_data: Dict[str, Any]) -> User:
        """Create user with hashed password."""
        password: str = validated_data.pop('password', None)
        user: User = User(**validated_data)

        if password:
            user.set_password(password)
        else:
            # For Telegram users without password
            user.set_unusable_password()

        user.save()
        return user


class LoginOrRegisterSerializer(serializers.Serializer):
    """
    Serializer for login or register via Telegram.
    """
    telegram_id = serializers.IntegerField(required=True)
    telegram_username = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    def validate_phone_number(self, value: str) -> str:
        """Validate phone number format."""
        if not value:
            return ''
        cleaned: str = value.replace(" ", "").replace("-", "")
        if not cleaned.startswith('+'):
            cleaned = f'+221{cleaned}'
        return cleaned


class LoginPasswordSerializer(serializers.Serializer):
    """
    Serializer for login with username/email and password.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate credentials."""
        from django.contrib.auth import authenticate

        username: str = attrs.get('username')
        password: str = attrs.get('password')

        # Try to authenticate
        user = authenticate(username=username, password=password)

        if not user:
            # Try with email
            user = User.objects.filter(email=username).first()
            if user and user.check_password(password):
                pass
            else:
                raise serializers.ValidationError(
                    "Identifiants invalides. Vérifiez votre nom d'utilisateur/email et mot de passe."
                )

        if not user.is_active:
            raise serializers.ValidationError(
                "Ce compte a été désactivé."
            )

        attrs['user'] = user
        return attrs
