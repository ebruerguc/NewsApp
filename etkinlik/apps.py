from django.apps import AppConfig


class EtkinlikConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'etkinlik'

    def ready(self):
        import etkinlik.signals
