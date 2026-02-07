from jwt.exceptions import ExpiredSignatureError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Intentar obtener el token de JWT desde la cookie
        token = request.COOKIES.get("access_token")
        if token is None:
            # APILogger.log_request("warning",
            #                       "No access token in cookie",
            #                       request,
            #                       {})
            return None  # Regresa None si no hay token, evitando continuar con el código

        try:
            # Validar el token usando el método de la clase base
            validated_token = self.get_validated_token(token)

            # ✅ Verificar si el token está en la blacklist usando hash del token
            from apps.authentication.models import TokenBlacklist
            import hashlib

            token_hash = hashlib.sha256(token.encode()).hexdigest()[:50]
            if TokenBlacklist.is_token_blacklisted(token_hash):
                # APILogger.log_request("warning", "Token is blacklisted", request, {"token_hash": token_hash})
                raise AuthenticationFailed("Este token ha sido revocado.")

        except ExpiredSignatureError:
            # APILogger.log_request("warning", "Token expired", request, {})
            raise AuthenticationFailed("Token expirado. Por favor, refresca tu token.")
        except InvalidToken:
            # APILogger.log_request("warning", "Invalid token", request, {})
            raise AuthenticationFailed("Token inválido.")

        user = self.get_user(validated_token)

        if user is None or not user.is_active:
            # APILogger.log_request("error", "Invalid token", request, {"validation_error": "User not found or inactive"})
            raise AuthenticationFailed("Token inválido o usuario inactivo")

        # APILogger.log_request("info", "Valid JWT token from cookie", request,
        #                       {"user_id": user.id, "username": user.username})

        return user, validated_token
