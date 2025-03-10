from rest_framework.response import Response
from rest_framework.mixins import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import DoctorsSpecialityInClinics, Consultation
from apps.core.permissions import IsAdmin, IsDoctor, IsPatient
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import ConsultationFilter
from .services import (
    get_consultation_data_allow_permission,
    user_create_consultation
)
from .serializers import (
    ConsultationChangeStatusSerializer,
    ConsultationSerializer,
    ConsultationDetailSerializer,
    DoctorsInClinicsSerializer
)
from rest_framework.exceptions import NotAuthenticated


class DoctorsInClinicsAPIView(generics.ListAPIView):
    """
    Контроллер вывода информации о врачах в клинике
    """
    queryset = DoctorsSpecialityInClinics.objects.all()
    serializer_class = DoctorsInClinicsSerializer
    permission_classes = [AllowAny]


class ConsultationCreateView(APIView):
    """
    Контроллер создания записи пациентом на консультацию
    """
    permission_classes = [IsPatient]

    def post(self, request):
        data = request.data.copy()
        data["patient"] = request.user.id
        return user_create_consultation(data)


class ConsultationListForDoctorsView(generics.ListAPIView):
    """
    Получение списка консультаций с поиском (пример: ?search=Иван),
    сортировкой по дате создания
    (?ordering=created_at или ?ordering=-created_at).
    Реализована функция фильтрации по статусу
    консультации(пример: ?status=confirmed).
    Разграничено предоставления доступа только врачам и админу.
    """
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ConsultationFilter
    ordering_fields = ['created_at']
    ordering = ['created_at']
    permission_classes = [IsAdmin | IsDoctor]


class ConsultationDetailView(generics.RetrieveAPIView):
    """
    Получение консультации по id
    """
    serializer_class = ConsultationDetailSerializer
    permission_classes = [IsAdmin | IsDoctor | IsPatient]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        queryset = get_consultation_data_allow_permission(user)
        if queryset:
            return queryset
        else:
            raise NotAuthenticated(
                "Вы не авторизованы для получения этих данных."
            )


class ConsultationUpdateView(generics.UpdateAPIView):
    """
    Редактирование консультации
    """
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAdmin | IsDoctor]
    lookup_field = 'id'
    http_method_names = ['put']


class ConsultationChangeStatusView(generics.RetrieveUpdateAPIView):
    """
    Редактирование статуса консультации
    """
    queryset = Consultation.objects.all()
    serializer_class = ConsultationChangeStatusSerializer
    permission_classes = [IsAdmin | IsDoctor]
    lookup_field = 'id'
    http_method_names = ['patch']


class ConsultationDeleteView(generics.DestroyAPIView):
    """
    Удаление консультации
    """
    queryset = Consultation.objects.all()
    permission_classes = [IsAdmin | IsDoctor]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"messages": "Запись успешно удалена"},
            status=status.HTTP_204_NO_CONTENT
        )
