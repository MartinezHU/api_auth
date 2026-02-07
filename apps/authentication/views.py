import datetime

from django.contrib.auth.hashers import check_password
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiParameter
from oauth2_provider.views import TokenView, IntrospectTokenView
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.authentication.models import APIUser
from apps.authentication.serializers import (
    APIUserRegistrationSerializer,
    OAuthTokenRequestSerializer,
    OAuthRevokeSerializer,
    APIUserSerializer,
    APITokenObtainPairSerializer,
    LogoutResponseSerializer,
    MeResponseSerializer,
)
from apps.authentication.tasks import send_user_to_queue
from apps.authentication.utils import generate_auth_token
from main.logging_config import log_api_call, APILogger


# Create your views here.


@extend_schema(
    tags=["SignUp"],
    summary="Registro de usuario",
    description="Endpoint para registro de usuarios.",
    responses={
        200: inline_serializer(
            name="SignUpResponseSerializer",
            fields={
                "message": serializers.CharField(),
                "app": serializers.CharField(),
                "access": serializers.CharField(),
                "refresh": serializers.CharField(),
            },
        ),
    },
    parameters=[
        OpenApiParameter(
            name="X-App-Name",
            type=OpenApiTypes.STR,
            location="header",
            description="Nombre de la aplicación cliente",
            required=True,
        )
    ],
)
class SignUpViewSet(ModelViewSet):
    queryset = APIUser.objects.none()
    serializer_class = APIUserRegistrationSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    @log_api_call(level="info")
    def create(self, request, *args, **kwargs):
        app_name = getattr(request, "app_name", None)
        auth_type = getattr(request, "auth_type", None)

        if not app_name or not auth_type:
            APILogger.log_request(
                "warning",
                "SingUp Failed: App name or auth type not provided",
                request,
                {"validation_error": "Missing app name or auth type"},
            )
            return Response(
                {"error": "No se ha proporcionado el nombre de la aplicación"},
                status=400,
            )

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # Actualizamos el nombre de la aplicación en el usuario
            user_update = APIUser.objects.get(id=user.id)

            if app_name in [choice[0] for choice in APIUser.APP_CHOICES]:
                user_update.origin_app = app_name
                user_update.save()

            # Log de creación de usuario exitosa
            APILogger.log_request(
                "info",
                f"User Created Successfully: {user.id}",
                request,
                {"user_id": str(user.id)},
            )

            # Generamos los tokens de autenticación según el tipo
            token_data = generate_auth_token(user, auth_type)

            response_data = {
                "message": "Usuario creado exitosamente",
                # Agregamos el nombre de la aplicación a la respuesta y los datos del token
                "app": app_name,
            }
            response_data.update(token_data)
            headers = self.get_success_headers(serializer.data)

            # Llamamos a la tarea de Celery para enviar los datos a RabbitMQ
            send_user_to_queue.delay(user.id, auth_type)

            return Response(response_data, headers=headers)

        except Exception:
            # El decorador log_api_call ya registra el error
            raise


class OAuthViews:
    """
    Vistas para el manejo de OAuth2.
    """

    class OAuthTokenEndpoint(TokenView, APIView):
        @extend_schema(
            operation_id="token_obtain_pair",
            summary="Obtener un token de acceso",
            description="""
                    Endpoint para obtener tokens OAuth2. Soporta los siguientes grant types:
                    - password: Para credenciales de usuario
                    - authorization_code: Para flujo de autorización
                    - refresh_token: Para renovar tokens
                    """,
            request=OAuthTokenRequestSerializer,
            responses={
                200: OAuthTokenRequestSerializer,
                # 400: OpenApiTypes.OBJECT,
                # 401: OpenApiTypes.OBJECT,
            },
            tags=["OAuth2"],
        )
        @log_api_call(level="info")
        def post(self, request, *args, **kwargs):
            return super().post(request, *args, **kwargs)

    class RevokeOAuthTokenEndpoint(APIView):
        @extend_schema(
            operation_id="revoke_token",
            summary="Revocar un token de acceso",
            description="Endpoint para revocar tokens OAuth2.",
            request=OAuthRevokeSerializer,
            responses={
                200: OpenApiTypes.OBJECT,
                # 400: OpenApiTypes.OBJECT,
                # 401: OpenApiTypes.OBJECT,
            },
            tags=["OAuth2"],
        )
        def post(self, request, *args, **kwargs):
            pass

    class IntrospectOAuthTokenEndpoint(APIView):
        permission_classes = [AllowAny]

        @extend_schema(
            operation_id="introspect_token",
            summary="Introspección de un token de acceso",
            description="Endpoint para introspección de tokens OAuth2.",
            request=inline_serializer(
                name="IntrospectTokenSerializer",
                fields={
                    "token": serializers.CharField(),
                },
            ),
            responses={
                200: OpenApiTypes.OBJECT,
                # 400: OpenApiTypes.OBJECT,
                # 401: OpenApiTypes.OBJECT,
            },
            tags=["OAuth2"],
        )
        @log_api_call(level="info")
        def post(self, request, *args, **kwargs):
            token = request.data.get("token")

            if not token:
                APILogger.log_request(
                    "warning",
                    "Introspection Failed: Token not provided",
                    request,
                    {"validation_error": "Token not provided"},
                )
                return Response({"error": "Token not provided"}, status=400)

            introspection_view = IntrospectTokenView.as_view()
            validate_data = {"token": token}
            request._data = validate_data  # Ensure the token is passed correctly

            return introspection_view(request, *args, **kwargs)


class JWTViews:
    """
    Vistas para el manejo de JWT.
    """

    @extend_schema(
        tags=["JWT"],
        summary="Obtener un par de tokens JWT",
        description="Endpoint para obtener un par de tokens de acceso y refresco JWT.",
        responses={200: OpenApiTypes.OBJECT},
        parameters=[
            OpenApiParameter(
                name="X-App-Name",
                type=OpenApiTypes.STR,
                location="header",
                required=True,
            )
        ],
    )
    class JWTObtainPairToken(TokenObtainPairView):
        serializer_class = APITokenObtainPairSerializer

        def post(self, request, *args, **kwargs):
            response = super().post(request, *args, **kwargs)
            app_name = getattr(request, "app_name", None)
            data = response.data

            user = APIUser.objects.filter(email=request.data.get("email")).first()
            if not user or not user.is_active:
                raise serializers.ValidationError("Usuario no válido o inactivo")

            if not check_password(request.data.get("password"), user.password):
                raise serializers.ValidationError("Credenciales inválidas")

            user_data = {
                "username": user.username if user.is_authenticated else None,
                "is_staff": user.is_staff,
            }

            response.set_cookie(
                key="app_name",
                value=app_name,
                expires=datetime.timedelta(days=7),
                secure=True,
                httponly=True,
                domain="localhost",
                samesite="None",  # O "Lax" si no necesitas acceso cross-origin estricto
            )

            response.set_cookie(
                key="access_token",
                value=data["access"],
                expires=datetime.timedelta(days=7),
                secure=True,
                httponly=True,
                domain="localhost",
                samesite="None",  # O "Lax" si no necesitas acceso cross-origin estricto
            )

            response.set_cookie(
                key="refresh_token",
                value=data["refresh"],
                expires=datetime.timedelta(days=30),
                secure=True,
                httponly=True,
                domain="localhost",
                samesite="None",  # O "Lax" si no necesitas acceso cross-origin estricto
            )

            # Combinar los datos originales con el mensaje
            response.data = {
                "message": "Token generado exitosamente",
                **data,
                **user_data,
            }
            return response

    @extend_schema(
        tags=["JWT"],
        summary="Renovar un token JWT",
        description="Endpoint para renovar un token JWT usando un token de refresco.",
        responses={200: OpenApiTypes.OBJECT},
    )
    class JWTRefreshToken(TokenRefreshView):
        def post(self, request, *args, **kwargs):
            try:
                response = super().post(request, *args, **kwargs)
                data = response.data

                response_data = {
                    "message": "Token refrescado exitosamente",
                    "access": data["access_token"],
                    "refresh": data["refresh_token"],
                }
                return Response(response_data)
            except serializers.ValidationError as e:
                # Capturar específicamente errores de token expirado o inválido
                if "token" in str(e).lower() or "invalid" in str(e).lower():
                    APILogger.log_request(
                        "warning",
                        "Token refresh failed - Invalid or expired refresh token",
                        request,
                        {"error": str(e)},
                    )
                    return Response(
                        {
                            "error": "Token de refresco inválido o expirado. Por favor, inicia sesión de nuevo.",
                            "detail": str(e)
                        },
                        status=401,
                    )
                raise

    @extend_schema(
        tags=["JWT"],
        summary="Revocar un token JWT",
        description="Endpoint para revocar un token JWT.",
        request=inline_serializer(
            name="RevokeTokenSerializer",
            fields={
                "token": serializers.CharField(),
            },
        ),
        responses={
            200: OpenApiTypes.OBJECT,
            # 400: OpenApiTypes.OBJECT,
            # 401: OpenApiTypes.OBJECT,
        },
    )
    class JWTRevokeToken(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request, *args, **kwargs):
            from apps.authentication.models import TokenBlacklist

            # Obtener token del body o de las cookies
            token = request.data.get("token") or request.COOKIES.get("access_token")
            refresh_token = request.data.get("refresh_token") or request.COOKIES.get("refresh_token")

            if not token and not refresh_token:
                APILogger.log_request(
                    "warning",
                    "Token revocation failed - Token not provided",
                    request,
                    {"validation_error": "Token not provided"},
                )
                return Response({"error": "Token no proporcionado"}, status=400)

            user_id = request.user.id
            revoked_count = 0

            # Revocar access token si existe
            if token:
                success = TokenBlacklist.revoke_token(token, user_id, "access")
                if success:
                    revoked_count += 1

            # Revocar refresh token si existe
            if refresh_token:
                success = TokenBlacklist.revoke_token(refresh_token, user_id, "refresh")
                if success:
                    revoked_count += 1

            if revoked_count > 0:
                APILogger.log_request(
                    "info",
                    f"Token(s) revoked successfully - Count: {revoked_count}",
                    request,
                    {"user_id": user_id, "revoked_count": revoked_count},
                )
                return Response(
                    {"message": f"Token(s) revocado(s) exitosamente ({revoked_count})"},
                    status=200
                )
            else:
                APILogger.log_request(
                    "warning",
                    "Token revocation failed - Unable to revoke tokens",
                    request,
                    {"user_id": user_id},
                )
                return Response(
                    {"error": "No se pudo revocar el token"},
                    status=400
                )


from rest_framework.generics import GenericAPIView


@extend_schema(
    tags=["User"],
    summary="Información del usuario actual",
    description="Endpoint para obtener información del usuario actual.",
    responses={
        200: inline_serializer(
            name="MeResponseSerializer",
            fields={
                "username": serializers.CharField(),
                "email": serializers.EmailField(),
                "origin_app": serializers.CharField(),
                "is_staff": serializers.BooleanField(),
            },
        )
    },
)
class MeView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeResponseSerializer

    def get(self, request):
        user_data = {
            "username": request.user.username,
            "email": request.user.email,
            "origin_app": request.user.origin_app,
            "is_staff": request.user.is_staff,
        }
        return Response(user_data)


@extend_schema(
    tags=["User"],
    summary="Cerrar sesión",
    description="Endpoint para cerrar sesión y eliminar cookies de autenticación.",
    responses={200: LogoutResponseSerializer},
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutResponseSerializer

    def post(self, request):
        from apps.authentication.models import TokenBlacklist

        APILogger.log_request(
            "info",
            "Logout request",
            request,
            {"user_id": request.user.id},
        )

        # Obtener tokens de las cookies
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")
        user_id = request.user.id

        # ✅ Revocar tokens JWT agregándolos a la blacklist
        revoked_count = 0
        if access_token:
            success = TokenBlacklist.revoke_token(access_token, user_id, "access")
            if success:
                revoked_count += 1

        if refresh_token:
            success = TokenBlacklist.revoke_token(refresh_token, user_id, "refresh")
            if success:
                revoked_count += 1

        # Eliminar las cookies
        response = Response(
            {
                "message": "Sesión cerrada exitosamente",
                "tokens_revoked": revoked_count
            },
            status=200
        )
        response.delete_cookie("app_name", domain="localhost")
        response.delete_cookie("access_token", domain="localhost")
        response.delete_cookie("refresh_token", domain="localhost")

        APILogger.log_request(
            "info",
            f"Logout successfully - Tokens revoked: {revoked_count}",
            request,
            {"user_id": user_id, "tokens_revoked": revoked_count},
        )

        return response


@extend_schema(
    tags=["User"],
    summary="Gestión de usuarios",
    description="Endpoint para la gestión de usuarios.",
    responses={200: APIUserSerializer},
    parameters=[
        OpenApiParameter(
            name="X-App-Name",
            type=OpenApiTypes.STR,
            location="header",
            description="Nombre de la aplicación cliente",
            required=True,
        )
    ],
)
class UserViewSet(ModelViewSet):
    queryset = APIUser.objects.all()
    serializer_class = APIUserSerializer
    permission_classes = [IsAuthenticated]
    scope_required = ["read", "write"]
    http_method_names = ["get", "put", "delete"]
