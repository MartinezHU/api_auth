from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter
from oauth2_provider import urls as oauth2_urls

from apps.authentication.views import (
    OAuth2TokenInstrospectionView,
    SignUpViewSet,
    VerifyJWTTokenView,
)

router = SimpleRouter()

router.register(r"signup", SignUpViewSet, basename="signup")

urlpatterns = [
    # Rutas para JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Rutas para OAuth2
    path("o/", include(oauth2_urls)),
    # Rutas de validación de tokens
    path("verify-token", VerifyJWTTokenView.as_view(), name="verify-token"),
    path(
        "introspect", OAuth2TokenInstrospectionView.as_view(), name="oauth2-introspec"
    ),
    path("", include(router.urls)),
]
