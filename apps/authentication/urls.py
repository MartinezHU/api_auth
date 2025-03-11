from django.urls import path, include
from oauth2_provider import urls as oauth2_urls
from oauth2_provider import views as oauth2_views
from rest_framework.routers import SimpleRouter

from apps.authentication.views import (
    SignUpViewSet,
    OAuthViews,
    JWTViews,
    UserViewSet,
    me,
    LogoutView,
)

router = SimpleRouter()

router.register(r"signup", SignUpViewSet, basename="signup")
router.register(r"users", UserViewSet, basename="users")
# router.register(r"logout", LogoutView, basename="logout")

urlpatterns = [
    # Rutas para JWT
    path("token/", JWTViews.JWTObtainPairToken.as_view(), name="token_obtain_pair"),
    path("token/refresh/", JWTViews.JWTRefreshToken.as_view(), name="token_refresh"),
    # Rutas para OAuth2
    # Incluye las siguientes rutas de django-oauth-toolkit:
    # - o/authorize/: Autorización del usuario para la aplicación cliente.
    # - o/token/: Obtención del token de acceso.
    # - o/revoke_token/: Revocación del token de acceso.
    # - o/applications/: Gestión de aplicaciones OAuth2 (usualmente para administradores).
    # - o/introspect/: Introspección del token.
    path(
        "o/",
        include(
            [
                path(
                    "token/",
                    OAuthViews.OAuthTokenEndpoint.as_view(),
                    name="token_obtain_pair",
                ),
                path(
                    "revoke_token/",
                    OAuthViews.RevokeOAuthTokenEndpoint.as_view(),
                    name="revoke_token",
                ),
                path(
                    "introspect/",
                    OAuthViews.IntrospectOAuthTokenEndpoint.as_view(),
                    name="introspect_token",
                ),
                path(
                    "authorize/",
                    oauth2_views.AuthorizationView.as_view(),
                    name="authorize",
                ),
                # Incluimos las rutas de applications con su namespace
                path(
                    "", include((oauth2_urls.management_urlpatterns, "oauth2_provider"))
                ),
            ]
        ),
    ),
    path("me/", me, name="me"),
    path("logout/", LogoutView.as_view(), name="me"),
    path("", include(router.urls)),
]
