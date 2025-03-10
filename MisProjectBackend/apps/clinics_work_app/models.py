from django.db import models
# from apps.core.models import Users


class Clinic(models.Model):
    """
    Модель клиники
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    legal_address = models.TextField(verbose_name='Юридический адрес')
    physical_address = models.TextField(verbose_name='Физический адрес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиника'
        verbose_name_plural = 'Клиники'


class DoctorsSpecialityInClinics(models.Model):
    """
    Модель специальности доктора с привязкой к клинике
    """
    doctor = models.ForeignKey(
        'core.Users',
        on_delete=models.CASCADE,
        related_name='doctor_at_clinic',
        verbose_name='Доктор'
    )
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name='clinic',
        verbose_name='Клиника'
    )
    specialty = models.CharField(max_length=100, verbose_name='Специальность')

    class Meta:
        verbose_name = 'Специализация доктора в клинике'
        verbose_name_plural = 'Специализации докторов в клинике'
        unique_together = ('doctor', 'clinic', 'specialty')


class Consultation(models.Model):
    """
    Модель консультации на приём к врачу
    """
    STATUS_CHOICES = (
            ('confirmed', 'Подтверждена'),
            ('pending', 'Ожидает'),
            ('started', 'Начата'),
            ('completed', 'Завершена'),
            ('paid', 'Оплачена'),
    )
    patient = models.ForeignKey(
        'core.Users',
        on_delete=models.CASCADE,
        related_name='patient_at_consultation',
        verbose_name='Пациент'
    )
    doctor_in_clinics = models.ForeignKey(
        DoctorsSpecialityInClinics,
        on_delete=models.CASCADE,
        related_name='doctor_at_consultation',
        verbose_name='Доктор'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'
