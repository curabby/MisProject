from typing import Any
from .models import Consultation
from apps.core.models import Users
from rest_framework.response import Response
from rest_framework.mixins import status
from .serializers import ConsultationSerializer


def get_consultation_data_allow_permission(user: Users) -> Consultation:
    """
    Обрабатывает права пользователя и в зависимости от роли
    возвращает выборку данных о консультациях: для сотрудников - полный доступ,
    для пациентов только свои записи
    """
    queryset = Consultation.objects.select_related(
        'patient',
        'doctor_in_clinics__doctor'
    )
    if not (user.is_admin or user.role.name == 'doctor'):
        queryset = queryset.filter(patient=user.pk)
        return queryset
    return queryset


def user_create_consultation(entered_data: Any) -> Response:
    try:
        serializer = ConsultationSerializer(data=entered_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        return Response(
            {"error": str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
