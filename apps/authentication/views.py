from django.utils.timezone import now
from requests import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken as AccessTokenJWT
from oauth2_provider.models import AccessToken as AccessTokenOAuth2
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import APIUser
from apps.authentication.serializers import APIUserRegistrationSerializer

# Create your views here.


class SignUpViewSet(ModelViewSet):
    queryset = APIUser.objects.none()
    serializer_class = APIUserRegistrationSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user=user)

        response_data = {
            "message": "Usuario creado exitosamente",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        headers = self.get_success_headers(serializer.data)

        return Response(response_data, headers=headers)


class VerifyJWTTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response(
                {"error": "Token requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            decoded_token = AccessTokenJWT(token=token)
            return Response({"valid": True, "user_id": decoded_token["user_id"]})
        except Exception as e:
            return Response(
                {"valid": False, "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED
            )


class OAuth2TokenInstrospectionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response(
                {"error": "Token requerido"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            access_token = AccessTokenOAuth2.objects.get(token=token)

            if access_token.expires < now():
                return Response(
                    {"valid": False, "error": "Token expirado"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            return Response(
                {
                    "valid": True,
                    "user_id": access_token.user.id,
                    "scope": access_token.scope,
                    "expires_in": (access_token.expires - now()).total_seconds(),
                }
            )

        except AccessTokenOAuth2.DoesNotExist:
            return Response(
                {"valid": False, "error": "Token inválido"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
