from rest_framework import serializers
from .models import (
    Consultation,
    DoctorsSpecialityInClinics,
)
from apps.core.models import Users


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'email', 'full_name', 'role']

    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name} {obj.middle_name}".strip()


class DoctorsInClinicsSerializer(serializers.ModelSerializer):
    doctor = UserSerializer(read_only=True)
    clinic = serializers.StringRelatedField()

    class Meta:
        model = DoctorsSpecialityInClinics
        fields = ['id', 'doctor', 'clinic', 'specialty']


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = [
            'id',
            'patient',
            'doctor_in_clinics',
            'created_at',
            'start_time',
            'end_time',
            'status'
        ]
        read_only_fields = ['created_at']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError(
                "Время окончания должно быть позже времени начала."
            )
        return data


class ConsultationChangeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['id', 'status']

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Consultation.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Недопустимый статус. Допустимые значения: {valid_statuses}"
            )
        return value


class ConsultationDetailSerializer(ConsultationSerializer):
    patient = UserSerializer(read_only=True)
    doctor_in_clinics = DoctorsInClinicsSerializer(read_only=True)

    class Meta(ConsultationSerializer.Meta):
        fields = ConsultationSerializer.Meta.fields + [
            'patient',
            'doctor_in_clinics'
        ]
