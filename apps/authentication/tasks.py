from celery import shared_task
from apps.authentication.models import APIUser

# TODO: Logging or email notification logic for queued events

"""
    This task sends user details to a queue for further processing.

    Args:
    user_id (int): The ID of the user to be processed.
    auth_type (str): The type of authentication used for the user.
"""


@shared_task(queue="user_queue")
def send_user_to_queue(user_id, auth_type):
    """
    Send user details to a queue for further processing.
    """

    # Fetch user details from the database and prepare the data to be sent to the queue
    user = APIUser.objects.get(id=user_id)

    user_data = {}

    if user:
        # Initialize user data dictionary with user details
        user_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            # 'created_at': user.created_at,
            'auth_type': auth_type,
        }

        print('User {} has been activated.'.format(user_data))

    return user_data
