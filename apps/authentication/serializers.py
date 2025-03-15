import re

from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import APIUser


class APIUserSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo de usuario API.
    """

    class Meta:
        model = APIUser
        fields = [
            "id",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "username",
            "origin_app",
        ]


class APIUserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializador para el registro de usuarios API.
    Maneja la validación y creación de nuevos usuarios.
    """

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=APIUser.objects.all(), message="El email ya está en uso"
            )
        ],
    )

    password1 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = APIUser
        fields = ["email", "password1", "password2"]

    @staticmethod
    def validate_password1(value):
        """
        Valida que la contraseña cumpla con los requisitos de seguridad.
        Utiliza una expresión regular para mayor eficiencia.
        """

        # Definimos los patrones de validación
        patterns = {
            r".{8,}": "La contraseña debe tener al menos 8 caracteres.",
            r"[A-Z]": "La contraseña debe contener al menos una letra mayúscula.",
            r"[a-z]": "La contraseña debe contener al menos una letra minúscula.",
            r'[!@#$%^&*(),.?":{}|<>]': "La contraseña debe contener al menos un signo de puntuación.",
        }

        # Validamos cada patrón
        for pattern, message in patterns.items():
            if not re.search(pattern, value):
                raise serializers.ValidationError(message)

        return value

    def validate(self, attrs):
        """
        Validar que las contraseñas coincidan y realizar validaciones adicionales si es necesario.
        """
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Las contraseñas no coinciden."})

        # Podemos agregar más validaciones cruzadas aquí si es necesario
        return attrs

    def create(self, validated_data):
        """
        Crea un nuevo usuario API con los datos validados.
        """
        try:
            validated_data.pop("password2")
            password = validated_data["password1"]

            user = APIUser.objects.create_user(
                email=validated_data["email"], password=password
            )
            return user
        except Exception as e:
            raise serializers.ValidationError(f"Error al crear el usuario: {e}") from e


class OAuthTokenRequestSerializer(serializers.Serializer):
    """
    Serializador para la solicitud de tokens OAuth2.
    """

    client_id = serializers.CharField(help_text="ID de la aplicación cliente")
    client_secret = serializers.CharField(
        help_text="Clave secreta de la aplicación cliente", required=False
    )

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
        required=False,
    )


class APITokenObtainPairSerializer(serializers.Serializer):
    """
    Serializador para la obtención de pares de tokens JWT.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Validamos que el usuario exista y esté activo
        user = APIUser.objects.filter(email=email).first()
        if not user or not user.is_active:
            raise serializers.ValidationError("Usuario no válido o inactivo")

        # Validamos que la contraseña sea correcta
        if not check_password(password, user.password):
            raise serializers.ValidationError("Contraseña incorrecta")

        # Generamos los tokens JWT
        refresh = RefreshToken.for_user(user)

        # Información adicional al token
        # if hasattr(user, 'profile'):
        #     refresh["role"] = user.profile.role
        #     refresh["permissions"] = list(user.get_all_permissions())

        data = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        return data
