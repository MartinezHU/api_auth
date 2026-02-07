"""
Comando de Django para limpiar tokens expirados de la blacklist.
Uso: python manage.py cleanup_expired_tokens
"""
from django.core.management.base import BaseCommand

from apps.authentication.models import TokenBlacklist


class Command(BaseCommand):
    help = 'Limpia tokens expirados de la blacklist'

    def handle(self, *args, **options):
        self.stdout.write('Limpiando tokens expirados...')

        # Obtener cuenta antes de limpiar
        from django.utils import timezone
        expired_count = TokenBlacklist.objects.filter(
            expires_at__lt=timezone.now()
        ).count()

        # Limpiar tokens expirados
        TokenBlacklist.cleanup_expired_tokens()

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Limpieza completada: {expired_count} token(s) expirado(s) eliminado(s)'
            )
        )
