import json
import logging
from datetime import datetime
from functools import wraps

# Configurar el logger principal
logger = logging.getLogger('api')


class APILogger:
    """
    Clase para registrar mensajes de log en la aplicación.
    """

    @staticmethod
    def get_request_data(request):
        """
        Extrae los datos de la solicitud HTTP.
        """
        return {
            'method': request.method,
            'path': request.path,
            'user_id': str(request.user.id) if request.user.is_authenticated else None,
            'ip': request.META.get('REMOTE_ADDR'),
            'app_name': getattr(request, 'app_name', None),
            'auth_type': getattr(request, 'auth_type', None),
            'headers': dict(request.headers),
            'query_params': dict(request.GET),
            # Evitar loguear datos sensibles
            'body': '[FILTERED]' if 'password' in request.data else request.data,
        }

    @staticmethod
    def format_log_message(message, extra_data):
        """
        Formatea el mensaje de log.
        """
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            **(extra_data or {}),
        }
        return json.dumps(log_data)

    @classmethod
    def log_request(cls, level, message, request, extra=None):
        """
        Registra un log con información de la request
        """
        request_data = cls.get_request_data(request)
        extra_data = {**request_data, **(extra if isinstance(extra, dict) else {})}
        formatted_message = cls.format_log_message(message, extra_data)

        getattr(logger, level)(formatted_message)


def log_api_call(level='info'):
    """
    Decorador para registrar logs de llamadas a la API.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(view_instance, request, *args, **kwargs):
            method_name = func.__name__
            view_name = view_instance.__class__.__name__

            APILogger.log_request(
                level,
                f"API Call Started: {view_name}.{method_name}",
                request,
                {'event_type': 'api_call_started'}
            )

            try:
                response = func(view_instance, request, *args, **kwargs)

                # Log de respuesta exitosa
                APILogger.log_request(
                    level,
                    f"API Call Finished: {view_name}.{method_name}",
                    request,
                    {
                        'event_type': 'request_completed',
                        'status_code': response.status_code,
                        'response_data': '[FILTERED]' if 'token' in response.data else response.data,
                    }
                )
                return response
            except Exception as e:
                # Log de error
                APILogger.log_request(
                    'error',
                    f"API Call Failed: {view_name}.{method_name}",
                    request,
                    {
                        'event_type': 'request_failed',
                        'error': str(e),
                        'error_type': e.__class__.__name__,
                    }
                )
                raise

        return wrapper

    return decorator
