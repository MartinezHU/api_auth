from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


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

        # Validar el token usando el método de la clase base
        validated_token = self.get_validated_token(token)
        user = self.get_user(validated_token)

        if user is None or not user.is_active:
            # APILogger.log_request("error", "Invalid token", request, {"validation_error": "User not found or inactive"})
            raise AuthenticationFailed("Invalid token")

        # APILogger.log_request("info", "Valid JWT token from cookie", request,
        #                       {"user_id": user.id, "username": user.username})

        return user, validated_token
