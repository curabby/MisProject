from rest_framework import generics
from rest_framework.permissions import AllowAny
from .permissions import IsAdmin
from .models import Users
from .serializers import (
    BaserUserCreateSerializer,
    DoctorCreateSerializer,
    CustomTokenObtainPairSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterPatientView(generics.CreateAPIView):
    """Регистрация пациентов"""
    queryset = Users.objects.all()
    serializer_class = BaserUserCreateSerializer
    permission_classes = [AllowAny]


class RegisterDoctorView(generics.CreateAPIView):
    """Регистрация докторов (только c правами админа)"""
    queryset = Users.objects.all()
    serializer_class = DoctorCreateSerializer
    permission_classes = [IsAdmin]


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Авторизация (получение JWT-токена).
    Добавляем информацию о роли в токен.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
