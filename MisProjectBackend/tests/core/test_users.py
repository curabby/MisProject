from typing import Any
import pytest
from rest_framework.test import APIClient
from apps.core.models import Role, Users
from rest_framework.response import Response

client = APIClient()


def create_roles() -> None:
    """
    Функция создания ролей
    """
    roles_data = [
        {'name': 'patient', 'defaults': {'description': 'Пациент'}},
        {'name': 'doctor', 'defaults': {'description': 'Доктор'}},
        {'name': 'admin', 'defaults': {'description': 'Администратор'}},
    ]
    for role_data in roles_data:
        Role.objects.get_or_create(**role_data)


def create_superuser_for_test() -> Any:
    """
    Создание тестового суперпользователя
    """
    superuser = Users.objects.create_superuser(
        email='super-user@admin.com',
        password='aDmin1234*',
        first_name='Admin',
        last_name='User',
        middle_name='Super',
        )
    return superuser


def get_user_data(role_name: str) -> dict[str, Any]:
    """
    Функция отдает данные тестового пользователя
    """
    payload = dict(
        first_name="Сергей",
        last_name="Иванов",
        middle_name="Алексеевич",
        email="sergeyTest@email.com",
        password="dsTestPswd1234*",
        phone="+79856652288"
    )
    if role_name == 'doctor':
        payload['first_name'] = 'Иван'
        payload['email'] = 'ivanTest@doctor.ru'
        payload['role'] = Role.objects.filter(name='doctor').first().pk
    return payload


def authorization_user(email: str, password: str) -> Any:
    """
    Функция авторизации пользователей, получение токена
    """
    response = client.post('/api/v1/users/login/', dict(
            email=email,
            password=password)
        )
    return response


def get_access_token_and_pass_to_header(auth_user_data: Any):
    """
    Получает access token и помещает его в хедер
    """
    access_token = auth_user_data.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')


@pytest.mark.django_db
def auth_admin() -> dict[str, str]:
    """
    Авторизация созданного тестовго суперпользователя,
    возвращаем токен авторизации
    """
    create_roles()
    create_superuser_for_test()
    auth_data = authorization_user('super-user@admin.com', 'aDmin1234*')
    return auth_data


def register_patient_or_doctor(role_name: str) -> Any:
    """
    Функция регистрация пациента или доктора
    """
    create_roles()
    payload_user_data = get_user_data(role_name)
    if role_name == 'doctor':
        get_access_token_and_pass_to_header(auth_admin())
    response_register_user = client.post(
        f"/api/v1/users/register/{role_name}/",
        payload_user_data)
    client.credentials()
    return response_register_user, payload_user_data


@pytest.mark.django_db
def test_register_patient() -> None:
    """
    Тест на регистрацию пациента
    """
    create_roles()
    response_register_user, payload_user_data = register_patient_or_doctor(
        'patient'
    )
    assert_to_register_users(1, response_register_user, payload_user_data)


@pytest.mark.django_db
def test_register_doctor() -> None:
    """
    Тест успешной регистрации доктора
    """
    create_roles()
    response_register_user, payload_user_data = register_patient_or_doctor(
        'doctor'
    )
    assert_to_register_users(2, response_register_user, payload_user_data)


@pytest.mark.django_db
def test_succsess_auth_patient() -> None:
    """
    Тест успешной авторизации пациента
    """
    _, payload_user_data = register_patient_or_doctor('patient')
    authorized_patient = authorization_user(
        payload_user_data['email'],
        payload_user_data['password']
    )
    assert authorized_patient.status_code == 200
    assert authorized_patient.data.get('access', 0) != 0


@pytest.mark.django_db
def test_unsuccsess_auth_patient() -> None:
    """
    Тест неудачной авторизации (не корректный пароль)
    """
    _, payload_user_data = register_patient_or_doctor('patient')
    authorized_patient = authorization_user(
        payload_user_data['email'],
        'UncorrectPassword'
    )
    assert authorized_patient.status_code == 401
    assert authorized_patient.get('access', 0) == 0


def assert_to_register_users(
        role: int,
        response_register_user: Response,
        payload_user_data: dict[str, Any]) -> None:
    """
    Функция осуществляющая проверку создания пользователей
    role: 1 - patient, 2 - doctor, 3 - admin
    """
    assert response_register_user.status_code == 201
    assert response_register_user.data is not None
    assert (
        response_register_user.data["first_name"]
    ) == payload_user_data["first_name"]
    assert response_register_user.data["role"] == role
    assert response_register_user.data.get("password", None) is None
