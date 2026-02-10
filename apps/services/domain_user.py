import requests

from apps.authentication.utils import generate_service_token


def notify_domain_user(user_id: str) -> None:
    service_token = generate_service_token(service_name='authentication-service', user_id=user_id)

    # Preparamos la petición HTTP para enviar la notificación al servicio de autenticación
    request = requests.post(
        url="http://localhost:8001/auth/create-domain-user/",
        headers={
            "Authorization": f"Bearer {service_token}",
            "Content-Type": "application/json"
        },
        #timeout=3,
    )

    if request.status_code != 200 and request.status_code != 201:
        raise Exception(f"Error al notificar al servicio de autenticación: {request.status_code} - {request.text}")
