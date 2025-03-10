from faker import Faker
from apps.clinics_work_app.models import Clinic

fake = Faker('ru_RU')


def create_fake_clinics(count=3):
    clinics = []
    for _ in range(count):
        clinic = Clinic.objects.create(
            name=fake.company(),
            legal_address=fake.address(),
            physical_address=fake.address()
        )
        clinics.append(clinic)
    return clinics
