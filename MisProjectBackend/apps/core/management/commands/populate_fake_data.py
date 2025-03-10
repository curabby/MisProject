from django.core.management.base import BaseCommand
from apps.core.models import Role
from apps.core.management.commands.populate_clinics import create_fake_clinics
from apps.core.management.commands.populate_users import create_fake_users
from apps.core.management.commands.populate_doctor_specialties import (
    create_doctor_specialties
)
from apps.core.management.commands.create_superuser import (
    create_superuser_handler
)


class Command(BaseCommand):
    """
    Заполняет базу данных фейковыми данными'
    """
    def handle(self, *args, **kwargs):
        # Создание базовых ролей
        Role.objects.get_or_create(
            name='patient',
            defaults={'description': 'Пациент'}
        )
        Role.objects.get_or_create(
            name='doctor',
            defaults={'description': 'Доктор'}
        )
        Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Администратор'}
        )
        # создание суперпользователя
        create_superuser_handler()
        # Создание клиник
        clinics = create_fake_clinics(3)
        print(f'Создано {len(clinics)} клиник')
        # Создание пациентов
        patients = create_fake_users('patient', 10)
        print(f'Создано {len(patients)} пациентов')
        # Создание врачей
        doctors = create_fake_users('doctor', 3)
        print(f'Создано {len(doctors)} врачей')
        # Привязка врачей к клиникам и специальностям
        specialties = [
            'Кардиолог',
            'Терапевт',
            'Хирург',
            'Невролог',
            'Офтальмолог'
        ]
        create_doctor_specialties(doctors, clinics, specialties)
        print('Специальности врачей добавлены')
        print('Генерация фейковых данных завершена!')
