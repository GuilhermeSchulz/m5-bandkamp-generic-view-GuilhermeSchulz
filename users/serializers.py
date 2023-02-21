from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_superuser",
        ]
        read_only_fields = ("id", "is_superuser")
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ]
            },
            "email": {
                "required": True,
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="This field must be unique.",
                    )
                ],
            },
        }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        password = self.context["request"].data.get("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            hash_pass = make_password(password)
            setattr(instance, "password", hash_pass)
        instance.save()

        return instance
