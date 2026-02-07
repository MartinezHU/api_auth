import os
from pathlib import Path

import environ

# Permite definir la ruta base del proyecto para construir rutas relativas: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Obtener variables de entorno desde el archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Utilizar la clase Env de django-environ para obtener variables de entorno
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# SECRET_KEY: clave secreta de Django para seguridad de la aplicación
SECRET_KEY = os.environ.get("SECRET_KEY")

# Importación de configuraciones específicas
from .installed_apps import INSTALLED_APPS
from .authentication import SIMPLE_JWT as JWT, OAUTH2_PROVIDER as OAUTH2, AUTH_METHODS_BY_APP as AUTH_METHODS
from .rest_framework import REST_FRAMEWORK as DRF_SETTINGS
from .swagger_doc import SPECTACULAR_SETTINGS as SWAGGER_SETTINGS
from .logging import LOGGING

INSTALLED_APPS = INSTALLED_APPS
SIMPLE_JWT = JWT
OAUTH2 = OAUTH2
AUTH_METHODS = AUTH_METHODS
REST_FRAMEWORK = DRF_SETTINGS
SWAGGER_SETTINGS = SWAGGER_SETTINGS
LOGGING = LOGGING

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Middleware para controlar la autenticación por aplicación cliente
    "apps.authentication.middlewares.AppAuthenticationMiddleware",
]

# URL de las rutas principales de la aplicación
ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"

# Configuración de la base de datos
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "authentication.APIUser"

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "es-es"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR.parent, "static")

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
# CELERY_TASK_DEFAULT_QUEUE = 'celery_queue'  # Cola predeterminada para tareas de Celery
# CELERY_TASK_ROUTES = {
#     'mi_app.tasks.send_user_to_queue': {'queue': 'celery_queue'},
#     # 'apps.notifications.tasks.*': {'queue': 'notifications_queue'}, # Definir la cola para tareas específicas
#     #...
# }

# CELERY_RESULT_BACKEND = 'disabled'  # Para almacenar resultados en lugar de enviarlos a un backend
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Para trabajar con el tiempo de espera, reintentos, etc.
# CELERY_TASK_ACKS_LATE = True  # Confirmar tareas después de que se hayan procesado
# CELERY_TIMEZONE = 'UTC'  # Ajusta la zona horaria si es necesario

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
