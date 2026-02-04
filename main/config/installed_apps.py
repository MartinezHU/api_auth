INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Aplicaciones de terceros
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "corsheaders",
    "rest_framework_simplejwt",
    "oauth2_provider",

    # Aplicaciones propias
    "apps.authentication",
]
