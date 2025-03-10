from rest_framework import serializers
from .models import Users, Role
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class BaserUserCreateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для создания пользователя по умолчанию с ролью пациент
    """
    class Meta:
        model = Users
        fields = [
            "id",
            "password",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone",
            "role"
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        if 'role' not in validated_data:
            role = Role.objects.get(name='patient')
            validated_data['role'] = role

        user = Users.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            role=validated_data['role']
        )
        return user


class DoctorCreateSerializer(BaserUserCreateSerializer):
    """
    Наследуемся от BaserUserCreateSerializer, и переназначаем роль на доктора
    """
    def create(self, validated_data):
        role = Role.objects.get(name='doctor')
        validated_data['role'] = role
        return super().create(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомизация токена с учетом роли пользователя
    """
    def get_token(self, user):
        token = super().get_token(user)
        token['role'] = user.role.name if user.role else None
        return token
