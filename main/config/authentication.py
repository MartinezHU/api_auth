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
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # "ROTATE_REFRESH_TOKENS": True,
    # "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,  # Clave secreta para firmar los tokens
    "ISSUER": "api_auth",  # Emisor del token
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_TYPE_CLAIM": "token_type",
    # "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_COOKIE": "access_token",  # Nombre de la cookie donde está el token
    "AUTH_COOKIE_SECURE": True,
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_SAMESITE": "None",
}

# Definimos los métodos de autenticación por aplicación (Actualizar según sea necesario)
AUTH_METHODS_BY_APP = {
    "mi_app_web": "jwt",
    "app_blog": "jwt",
    "api_tienda": "oauth2",
    "mi_app_externa": "firebase",
}
