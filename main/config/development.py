from corsheaders.defaults import default_headers

from .base import *

# Configuraciones específicas para desarrollo

DEBUG = True
ALLOWED_HOSTS = ["*"]  # Permitir cualquier host en desarrollo

# Configuración de CORS para desarrollo

CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "X-App-Name",
]
