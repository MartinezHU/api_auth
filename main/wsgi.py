"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import logging.config
from pathlib import Path
import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.config.development')

# Obtener la ruta del directorio raíz del proyecto
project_root = Path(__file__).resolve().parent.parent

# Construir la ruta al archivo logging.ini
logging_config_path = project_root / 'logging.ini'

application = get_wsgi_application()
