"""
Extensiones de drf-spectacular para autenticación personalizada.
"""
from drf_spectacular.extensions import OpenApiAuthenticationExtension

from apps.authentication.authentication import CookieJWTAuthentication


class CookieJWTAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = CookieJWTAuthentication
    name = "cookieJWT"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token stored in 'access_token' cookie. "
                           "Obtain via login endpoint.",
        }
