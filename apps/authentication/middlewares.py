from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class AppAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        Middleware para obtener el nombre de la aplicación y el tipo de autenticación
        desde el encabezado 'X-App-Name'.
        """

        if request.path.startswith(
            ("/api/v1/auth/signup/", "/api/v1/auth/users/", "/api/v1/auth/token")
        ):
            app_name = request.headers.get("X-App-Name")

            if not app_name:
                return JsonResponse(
                    {"error": "No se ha proporcionado el nombre de la aplicación"},
                    status=400,
                )

            if request.path.startswith(("/api/v1/auth/signup/", "/api/v1/auth/token")):

                if app_name not in settings.AUTH_METHODS:
                    return JsonResponse(
                        {"error": "La aplicación no está registrada"}, status=400
                    )

                self._set_app_data(request, app_name)

    @staticmethod
    def _set_app_data(request, app_name):
        """
        Establece los datos de la aplicación en el objeto request.
        """

        request.app_name = app_name
        request.auth_type = settings.AUTH_METHODS[app_name]
