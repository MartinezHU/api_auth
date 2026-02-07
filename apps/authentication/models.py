from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.


class APIUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class APIUser(AbstractBaseUser, PermissionsMixin):
    # Aquí se definirán las apps clientes
    APP_CHOICES = [("pedidos", "PEDIDOS"), ("mi_app_web", "MI APP WEB"), ("api_blog", "API BLOG")]
    email = models.EmailField(unique=True)
    # Campo para el username
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    origin_app = models.CharField(
        max_length=50, choices=APP_CHOICES, blank=True, null=True
    )

    objects = APIUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """Genera un username si no se proporciona"""
        if not self.username:
            # Usa la parte antes del @ como base
            base_username = self.email.split("@")[0]
            self.username = f"user_{self.id}" if self.id else base_username
        super().save(*args, **kwargs)


class TokenBlacklist(models.Model):
    """
    Modelo para almacenar tokens revocados (logout, cambio de contraseña, etc.)
    """
    jti = models.CharField(
        max_length=50,
        unique=True,
        help_text="Hash SHA256 del token (50 caracteres)"
    )
    token = models.TextField(help_text="Token completo")
    user_id = models.IntegerField(help_text="ID del usuario asociado al token")
    token_type = models.CharField(
        max_length=20,
        choices=[("access", "Access"), ("refresh", "Refresh")],
        help_text="Tipo de token",
        default="access"
    )
    revoked_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="Fecha de expiración original del token")

    class Meta:
        db_table = "token_blacklist"
        verbose_name = "Token Revocado"
        verbose_name_plural = "Tokens Revocados"
        ordering = ["-revoked_at"]  # Más recientes primero
        indexes = [
            models.Index(fields=["jti"]),
            models.Index(fields=["user_id"]),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self):
        return f"Token {self.token_type} - Usuario {self.user_id} - {self.revoked_at}"

    @classmethod
    def is_token_blacklisted(cls, jti):
        """Verifica si un token con el JWT ID dado está en la lista negra"""
        return cls.objects.filter(jti=jti).exists()

    @classmethod
    def revoke_token(cls, token, user_id, token_type="access"):
        """Agrega un token a la lista negra"""

        import jwt
        import hashlib
        from datetime import datetime
        from django.utils import timezone
        from main.config.base import SECRET_KEY
        from main.config.authentication import SIMPLE_JWT

        try:
            # Usar hash del token como identificador único consistente
            jti = hashlib.sha256(token.encode()).hexdigest()[:50]

            # Decodificar para obtener la fecha de expiración
            decoded = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[SIMPLE_JWT["ALGORITHM"]]
            )

            # Convertir timestamp a datetime timezone-aware
            exp_timestamp = decoded.get("exp")
            expires_at = timezone.make_aware(datetime.fromtimestamp(exp_timestamp))

            obj, created = cls.objects.get_or_create(
                jti=jti,
                defaults={
                    "token": token,
                    "user_id": user_id,
                    "token_type": token_type,
                    "expires_at": expires_at,
                }
            )

            if not created:
                print(f"Token ya estaba en blacklist: {jti}")

            return True
        except Exception as e:
            print(f"Error revocando token: {e}")
            import traceback
            traceback.print_exc()
            return False

    @classmethod
    def cleanup_expired_tokens(cls):
        """Elimina tokens revocados que ya han expirado para mantener la base de datos limpia"""
        from django.utils import timezone
        cls.objects.filter(expires_at__lt=timezone.now()).delete()
