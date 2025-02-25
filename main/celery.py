from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.config.development')

# Crear una instancia de Celery
app = Celery('main')

# Usa el string de configuración para configurar el backend y el broker
app.config_from_object('django.conf:settings', namespace='CELERY')

# Registra todas las tareas de la aplicación
app.autodiscover_tasks()

# Opcional: para debugging
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')