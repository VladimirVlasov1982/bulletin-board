from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    """
    Сериализатор регистрации пользователя
    """
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone = PhoneNumberField(null=False, blank=False)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    class Meta():
        model = User
        fields = ["email", "first_name", "last_name", "password", "phone", "image"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class CurrentUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя
    """
    id = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "id", "email", "image"]
