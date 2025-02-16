from .base import *

# Configuraciones específicas para desarrollo

DEBUG = True
ALLOWED_HOSTS = ["*"]  # Permitir cualquier host en desarrollo

# Configuración de CORS para desarrollo
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = ['http://localhost:4200']

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

INSTALLED_APPS += [
    # Aquí se pueden agregar aplicaciones específicas para desarrollo
]

# Aquí se pueden insertar middlewares específicos para desarrollo
# MIDDLEWARE.insert()

# Configuración de la base de datos para desarrollo
# DATABASES["default"]["HOST"] = "localhost"
# DATABASES["default"]["PORT"] = "5432"
