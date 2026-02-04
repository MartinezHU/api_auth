from corsheaders.defaults import default_headers

from .base import *

# Configuraciones específicas para desarrollo

DEBUG = True
ALLOWED_HOSTS = ["*"]  # Permitir cualquier host en desarrollo

# Configuración de CORS para desarrollo

CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = ['http://localhost:4200', "http://localhost:5173", "https://localhost:5174",
                        "https://localhost:5173", "https://localhost:5173"]

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

INSTALLED_APPS += [
    # Aquí se pueden agregar aplicaciones específicas para desarrollo
    "django_extensions",
    # "debug_toolbar",
    # "django_pdb",
    # "rest_framework_swagger",
    # "drf_yasg",
    # "storages",
    # "rest_framework_simplejwt",
    # "corsheaders",
    # "django_filters",
    # "django_celery_beat",
    # "django_celery_results",
    # "channels",
    # "channels_redis",
    # "django_storages",
    # "django_storages_s3",
    # "storages_backends.gcloud",
    # "storages.backends.gcloud.GoogleCloudStorage",
    # "storages.backends.gcloud.GoogleCloudStorageAuth",
    # "storages.backends.gcloud.GoogleCloudStoragePipeline",
    # "storages.backends.gcloud.GoogleCloudStorageS3Boto3",
]

# Aquí se pueden insertar middlewares específicos para desarrollo
# MIDDLEWARE.insert()

# Configuración de la base de datos para desarrollo
# DATABASES["default"]["HOST"] = "localhost"
# DATABASES["default"]["PORT"] = "5432"
