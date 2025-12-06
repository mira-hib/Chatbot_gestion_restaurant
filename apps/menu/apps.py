from django.apps import AppConfig


class MenuConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'apps.menu'
    verbose_name: str = 'Menu'
