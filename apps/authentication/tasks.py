import json

import pika
from celery import shared_task
from apps.authentication.models import APIUser

# TODO: Logging or email notification logic for queued events

"""
    This task sends user details to a queue for further processing.

    Args:
    user_id (int): The ID of the user to be processed.
    auth_type (str): The type of authentication used for the user.
"""


@shared_task
def send_user_to_queue(user_id, auth_type):
    """
    Celery task to prepare user data and send it directly to user_queue as JSON.
    """
    # Fetch user details from the database
    try:
        user = APIUser.objects.get(id=user_id)
    except APIUser.DoesNotExist:
        print(f"User with id {user_id} not found.")
        return None

    # Prepare user data dictionary
    user_data = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'auth_type': auth_type,
    }

    print(f"User {user_data['username']} has been prepared.")

    # Conectar a RabbitMQ y enviar user_data a user_queue
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declarar la cola
    channel.queue_declare(queue='user_queue', durable=True)

    # Serializar user_data a JSON
    message = json.dumps(user_data)

    # Publicar el mensaje en user_queue
    channel.basic_publish(
        exchange='',
        routing_key='user_queue',
        body=message.encode('utf-8'),
        properties=pika.BasicProperties(delivery_mode=2)  # Mensaje persistente
    )

    print(f" [x] Sent user data to user_queue: '{message}'")

    # Cerrar la conexión
    channel.close()
    connection.close()

    return user_data