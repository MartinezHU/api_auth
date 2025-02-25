from datetime import timedelta

from main.config.base import SECRET_KEY


# Configuración de autenticación por aplicación OAuth2 (OAuth Toolkit)
OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_EXPIRE_SECONDS": 2592000,
    "AUTHORIZATION_CODE_EXPIRE_SECONDS": 600,
    "CLIENT_ID_GENERATOR_CLASS": "oauth2_provider.generators.ClientIdGenerator",
    "CLIENT_SECRET_GENERATOR_CLASS": "oauth2_provider.generators.ClientSecretGenerator",
    "ALLOWED_GRANT_TYPES": ["password", "authorization_code", "refresh_token"],
    "SCOPES": {
        "read": "Read access",
        "write": "Write access",
    },
}


# Configuración de autenticación JWT (Simple JWT)
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),  # Duración del token de acceso
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Duración del token de refresco
#     "ROTATE_REFRESH_TOKENS": True,  # Rotar tokens de refresco en cada solicitud
#     "BLACKLIST_AFTER_ROTATION": True,  # Invalidar el token de refresco anterior después de la rotación
#     "UPDATE_LAST_LOGIN": False,  # Actualizar la última fecha de inicio de sesión
#     "ALGORITHM": "HS256",  # Algoritmo de firma (recomendado HS256 o RS256)
#     "SIGNING_KEY": SECRET_KEY,  # Clave secreta para firmar los tokens (usa la misma que SECRET_KEY o una diferente)
#     # "VERIFYING_KEY": None, # Clave pública para verificar los tokens (necesaria si usas RS256)
#     "AUDIENCE": None,  # Audiencia del token (opcional)
#     "ISSUER": "api_auth",  # Emisor del token (opcional)
#     "JWK_URL": None,
#     # URL para obtener la clave pública en formato JWK (necesaria si usas RS256 y la clave no está en el archivo)
#     "LEEWAY": 0,  # Tolerancia de tiempo para la validación de tokens (opcional)
#     "AUTH_HEADER_TYPES": ("Bearer",),  # Tipo de encabezado de autorización
#     "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",  # Nombre del encabezado de autorización
#     "USER_ID_FIELD": "id",  # Campo que identifica al usuario en el token
#     "USER_ID_CLAIM": "user_id",  # Nombre del claim que contiene el ID del usuario en el token
#     "AUTH_TOKEN_CLASSES": (
#         "rest_framework_simplejwt.tokens.AccessToken",
#     ),  # Clases de tokens a usar
#     "TOKEN_TYPE_CLAIM": "token_type",  # Nombre del claim que contiene el tipo de token
#     "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
#     # Nombre del claim que contiene la fecha de expiración del token de refresco
#     "SLIDING_TOKEN_LIFETIME": timedelta(
#         minutes=60
#     ),  # Duración del token de acceso con refresh sliding
#     "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(
#         days=1
#     ),  # Duración del token de refresco con refresh sliding
# }

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,  # Clave secreta para firmar los tokens
    "ISSUER": "api_auth",  # Emisor del token
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_TYPE_CLAIM": "token_type",
}

# Definimos los métodos de autenticación por aplicación (Actualizar según sea necesario)
AUTH_METHODS_BY_APP = {
    "mi_app_web": "jwt",
    "api_blog": "jwt",
    "api_tienda": "oauth2",
    "mi_app_externa": "firebase",
}
