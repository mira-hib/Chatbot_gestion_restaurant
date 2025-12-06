from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'apps.orders'
    verbose_name: str = 'Commandes'
