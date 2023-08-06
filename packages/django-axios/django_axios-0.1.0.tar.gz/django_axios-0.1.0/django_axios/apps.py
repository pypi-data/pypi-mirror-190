from django.apps import AppConfig

from .socket import ready

class DjangoAxiosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_axios'

    def ready(self) -> None:
        return ready()