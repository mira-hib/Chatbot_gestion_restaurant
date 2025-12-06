"""
Django settings for Restaurant Chatbot project.
"""
import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = os.getenv(
    'SECRET_KEY',
    'django-insecure-dev-key-change-in-production'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS: List[str] = ["*"]

# Application definition
INSTALLED_APPS: List[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_spectacular',

    # Local apps
    'apps.core',
    'apps.users',
    'apps.menu',
    'apps.orders',
    'apps.wallet',
]

MIDDLEWARE: List[str] = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF: str = 'config.urls'

TEMPLATES: List[dict] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION: str = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / os.getenv('DATABASE_NAME', 'db.sqlite3'),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS: List[dict] = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE: str = 'fr-fr'
TIME_ZONE: str = 'Africa/Dakar'
USE_I18N: bool = True
USE_TZ: bool = True


# Static files (CSS, JavaScript, Images)
STATIC_URL: str = 'static/'
STATIC_ROOT: Path = BASE_DIR / 'staticfiles'
STATICFILES_DIRS: List[Path] = [BASE_DIR / 'static']

# Media files
MEDIA_URL: str = 'media/'
MEDIA_ROOT: Path = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL: str = 'users.User'


# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.core.authentication.BearerTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# drf-spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Restaurant Chatbot API',
    'DESCRIPTION': 'API pour la gestion des commandes restaurant via Telegram Bot',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/',
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY': [
        {
            'tokenAuth': [],
        },
        {
            'basicAuth': [],
        }
    ],
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'tokenAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'Token',
                'description': 'Token authentication: Just paste your token (without "Token" or "Bearer" prefix)'
            },
            'basicAuth': {
                'type': 'http',
                'scheme': 'basic',
                'description': 'Basic HTTP authentication (for admin)'
            }
        }
    }
}

# CORS settings
CORS_ALLOWED_ORIGINS: List[str] = [
    'http://localhost:3000',
    'http://localhost:5678',  # n8n
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5678',
    'https://django.ibson.online',
]

CORS_ALLOW_CREDENTIALS: bool = False

# Wave API Configuration
WAVE_API_URL: str = os.getenv('WAVE_API_URL', '')
WAVE_API_KEY: str = os.getenv('WAVE_API_KEY', '')
WAVE_API_SECRET: str = os.getenv('WAVE_API_SECRET', '')
