import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.authentication.models import APIUser


class APIUserSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo de usuario API.
    """
    class Meta:
        model = APIUser
        fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser', 'username', 'origin_app']


class APIUserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializador para el registro de usuarios API.
    Maneja la validación y creación de nuevos usuarios.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=APIUser.objects.all(),
            message="El email ya está en uso"
        )]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = APIUser
        fields = ['email', 'password']

    @staticmethod
    def validate_password(value):
        """
        Valida que la contraseña cumpla con los requisitos de seguridad.
        Utiliza una expresión regular para mayor eficiencia.
        """

        # Definimos los patrones de validación
        patterns = {
            r'.{8,}': "La contraseña debe tener al menos 8 caracteres.",
            r'[A-Z]': "La contraseña debe contener al menos una letra mayúscula.",
            r'[a-z]': "La contraseña debe contener al menos una letra minúscula.",
            r'[!@#$%^&*(),.?":{}|<>]': "La contraseña debe contener al menos un signo de puntuación."
        }

        # Validamos cada patrón
        for pattern, message in patterns.items():
            if not re.search(pattern, value):
                raise serializers.ValidationError(message)

        return value

    def create(self, validated_data):
        """
        Crea un nuevo usuario API con los datos validados.
        """
        try:
            return APIUser.objects.create_user(
                email=validated_data['email'], password=validated_data['password']
            )
        except Exception as e:
            raise serializers.ValidationError(f"Error al crear el usuario: {e}") from e


class OAuthTokenRequestSerializer(serializers.Serializer):
    """
    Serializador para la solicitud de tokens OAuth2.
    """

    client_id = serializers.CharField(help_text="ID de la aplicación cliente")
    client_secret = serializers.CharField(help_text="Clave secreta de la aplicación cliente", required=False)

    username = serializers.CharField(help_text="Email del usuario", required=False)
    password = serializers.CharField(help_text="Contraseña del usuario", required=False)

    code = serializers.CharField(help_text="Código de autorización", required=False)
    redirect_uri = serializers.CharField(help_text="URI de redirección", required=False)

    grant_type = serializers.ChoiceField(
        choices=["password", "authorization_code", "refresh_token"],
        help_text="Tipo de grant OAuth2",
    )

    scope = serializers.CharField(help_text="Scopes solicitados", required=False)


class OAuthTokenResponseSerializer(serializers.Serializer):
    """
    Serializador para la respuesta de tokens OAuth2.
    """

    access_token = serializers.CharField()
    token_type = serializers.CharField()
    expires_in = serializers.IntegerField()
    refresh_token = serializers.CharField()
    scope = serializers.CharField()


class OAuthRevokeSerializer(serializers.Serializer):
    """
    Serializador para la revocación de tokens OAuth2.
    """

    token = serializers.CharField(help_text="Token a revocar")
    token_type_hint = serializers.ChoiceField(
        choices=["access_token", "refresh_token"],
        help_text="Tipo de token a revocar",
        required=False
    )
