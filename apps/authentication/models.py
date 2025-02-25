from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.template.defaultfilters import first


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
