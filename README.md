# API de Autenticación Centralizada

Un servicio de autenticación basado en Django REST Framework diseñado para proyectos personales, que permite múltiples
métodos de autenticación dependiendo de la aplicación que lo consuma.

## Características

- Servicio de autenticación centralizado para múltiples aplicaciones
- Registro y gestión de usuarios
- Compatible con múltiples métodos de autenticación:
    - OAuth2 (password, authorization_code, refresh_token)
    - JWT (tokens de acceso y refresco)
- Introspección de tokens para validación segura
- Registro de usuarios basado en la aplicación que consume la API mediante el encabezado X-App-Name
- Registro detallado de eventos y monitoreo de seguridad
- Documentación OpenAPI con drf-spectacular (Swagger UI)
- Gestion de cola de mensajes con RabbitMQ

## Tecnologías utilizadas

- Python
- Django
- Django REST Framework
- Django OAuth Toolkit
- Simple JWT
- drf-spectacular (para documentación OpenAPI)

## Endpoints de la API

### Autenticación

#### Registro de usuario

- `POST /signup/`
    - Registra nuevos usuarios
    - Requiere el encabezado X-App-Name

#### OAuth2

- `POST /o/token/`
    - Obtiene tokens de acceso OAuth2
    - Soporta múltiples tipos de flujo
- `POST /o/revoke_token/`
    - Revoca tokens OAuth2
- `POST /o/introspect/`
    - Verifica la validez de un token OAuth2

#### JWT (JSON Web Token)

- `POST /token/`
    - Obtiene tokens de acceso y refresco JWT
- `POST /token/refresh/`
    - Renueva tokens JWT

### User Management

- `GET /users/`
    - Lista todos los usuarios (requiere autenticación)
- `GET /users/{id}/`
    - Obtiene detalles de un usuario específico
- `PUT /users/{id}/`
    - Actualiza la información de un usuario
- `DELETE /users/{id}/`
    - Elimina un usuario

## Seguridad

- Autenticación obligatoria para los endpoints de gestión de usuarios
- Sistema de permisos basado en alcances (scopes)
- Registro de solicitudes y monitoreo de seguridad

## Instalación

1. Clonar el repositorio:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3. Crear un archivo `.env` y definir las variables de entorno necesarias.

4. Crear la carpeta `logs/`:
    ```bash
    mkdir logs
    ```

5. Crear y ejecutar las migraciones de la base de datos:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Crear contenedor de RabbitMQ:
    ```bash
    docker run --name rabbitmq-container -p 5672:5672 -p 15672:15672 -d rabbitmq:management
    ```

7. En caso de despliegue, configurar `wsgi.py` correctamente según el servidor o proyecto.

### Por implementar

1. Gestión persistente de la cosa de mensajes con RabbitMQ (Permitir reintentos, recuperación de cola, etc.)
2. Implementar autenticación con otros métodos de autenticación (Google, Facebook, etc.)
3. Mejorar gestión de usuarios y roles (crear permisos más granulares, etc.)