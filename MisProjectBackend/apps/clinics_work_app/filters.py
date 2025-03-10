import django_filters
from .models import Consultation
from django.db.models import Q


class ConsultationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_by_search', label="Поиск по имени врача или пациента"
    )

    class Meta:
        model = Consultation
        fields = ['status', 'created_at']

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(patient__first_name__icontains=value) |
            Q(patient__last_name__icontains=value) |
            Q(patient__middle_name__icontains=value) |
            Q(doctor_in_clinics__doctor__first_name__icontains=value) |
            Q(doctor_in_clinics__doctor__last_name__icontains=value) |
            Q(doctor_in_clinics__doctor__middle_name__icontains=value)
        )
