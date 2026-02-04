import datetime
import uuid
from enum import Enum

from oauth2_provider.models import AccessToken as OAuthAccessToken, RefreshToken as OAuthRefreshToken, Application
from rest_framework_simplejwt.tokens import RefreshToken as JWTRefreshToken, AccessToken as JWTAccessToken


class AuthType(Enum):
    JWT = "jwt"
    OAUTH2 = "oauth2"
    FIREBASE = "firebase"


def generate_auth_token(user, auth_type: str):
    """
    Genera un token de autenticación según el tipo de autenticación.

    Args:
        user: Usuario para el que se generará el token
        auth_type: Tipo de autenticación ('jwt', 'oauth2', 'firebase')

    Returns:
        dict: Diccionario con tokens de acceso y refresco

    Raises:
        ValueError: Si el tipo de autenticación no es válido o hay errores de configuración
        NotImplementedError: Sí se intenta usar autenticación Firebase
    """
    auth_type = auth_type.lower()
    if auth_type not in AuthType._value2member_map_:
        raise ValueError(f"Tipo de autenticación no soportado. Valores válidos: {[t.value for t in AuthType]}")

    try:
        if auth_type == AuthType.JWT.value:
            return generate_jwt_token(user)
        elif auth_type == AuthType.OAUTH2.value:
            return generate_oauth2_token(user)
        elif auth_type == AuthType.FIREBASE.value:
            raise NotImplementedError("Autenticación con Firebase no implementada")
    except Application.DoesNotExist as e:
        raise ValueError("Aplicación OAuth2 no configurada correctamente")
    except Exception as e:
        raise ValueError(f"Error al generar token: {str(e)}")


def generate_jwt_token(user):
    refresh = JWTRefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def generate_oauth2_token(user):
    application = Application.objects.get(name="api_auth")
    expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
    access_token = OAuthAccessToken.objects.create(
        user=user,
        application=application,
        expires=expires,
        token=f"oauth2_{user.id}_{uuid.uuid4()}",
    )
    refresh_token = OAuthRefreshToken.objects.create(
        user=user,
        token=f"oauth2_refresh_{user.id}_{uuid.uuid4()}",
        access_token=access_token,
        application=application,
    )
    return {
        "access": access_token.token,
        "refresh": refresh_token.token,
        "expires": expires.timestamp(),
    }
