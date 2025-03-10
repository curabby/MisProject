import random
from apps.clinics_work_app.models import DoctorsSpecialityInClinics


def create_doctor_specialties(doctors, clinics, specialties):
    for doctor in doctors:
        num_clinics = random.randint(1, min(2, len(clinics)))  # 1-2 клиники
        selected_clinics = random.sample(clinics, num_clinics)
        for clinic in selected_clinics:
            num_specialties = random.randint(1,
                                             min(3, len(specialties)
                                                 ))  # 1-3 специальности
            selected_specialties = random.sample(specialties, num_specialties)
            for specialty in selected_specialties:
                DoctorsSpecialityInClinics.objects.get_or_create(
                    doctor=doctor,
                    clinic=clinic,
                    specialty=specialty
                )
