from faker import Faker
from apps.core.models import Role, Users

fake = Faker('ru_RU')


def create_fake_users(role_name, count):
    role = Role.objects.get(name=role_name)
    users = []
    for _ in range(count):
        user = Users.objects.create_user(
            email=fake.email(),
            password='password123',
            role=role,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            middle_name=fake.middle_name(),
            phone=fake.phone_number()
        )
        users.append(user)
    return users
