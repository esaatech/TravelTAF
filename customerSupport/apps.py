from django.apps import AppConfig


class CustomersupportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customerSupport'

    def ready(self):
        try:
            import customerSupport.signals  # Register signals
        except ImportError:
            pass
