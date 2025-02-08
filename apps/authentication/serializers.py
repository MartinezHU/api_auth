import re
import string
from rest_framework import serializers
from django import db

from apps.authentication.models import APIUser


class APIUserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = APIUser
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get("password")

        if APIUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "El email ya está en uso"})

        self.validate_username(username)
        self.validate_password(password)

        return attrs

    def create(self, validated_data):
        """Crear el usuario y devolver tokens"""
        with db.transaction.atomic():
            user = APIUser.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
            )

        return user

    def validate_username(self, value):
        if value is not None and value.strip() != "":
            if not re.match(r"^[a-zA-Z0-9_.-]{5,16}$", value):
                raise serializers.ValidationError(
                    "El nombre de usuario debe contener entre 5 y 16 caracteres y solo puede incluir letras, números, "
                    "guiones bajos, puntos y guiones."
                )
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "La contraseña debe tener al menos 8 caracteres."
            )
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra mayúscula."
            )
        if not any(char.islower() for char in value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra minúscula."
            )
        if not any(char in string.punctuation for char in value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un signo de puntuación."
            )
        return value
