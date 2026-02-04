from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentication'

    def ready(self):
        # Importamos la extensión de drf-spectacular para la autenticación personalizada
        try:
            import apps.authentication.authentication_extensions  # noqa: F401
        except ImportError:
            pass
