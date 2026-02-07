from .base import *

# Configuraciones específicas para producción
DEBUG = False

# Lista de hosts permitidos en producción
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

# Configuración de la base de datos para producción
DATABASES["default"]["HOST"] = os.getenv("DB_HOST", "db_production")
DATABASES["default"]["PORT"] = os.getenv("DB_PORT", "5432")

# Configuración de seguridad
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
