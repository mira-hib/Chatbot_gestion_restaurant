from django.apps import AppConfig


class WalletConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'apps.wallet'
    verbose_name: str = 'Portefeuille'
