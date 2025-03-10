from typing import Any
from apps.clinics_work_app.models import (
    Consultation,
    DoctorsSpecialityInClinics
)
from apps.core.models import Users
from tests.core.test_users import (
    client,
    get_access_token_and_pass_to_header,
    register_patient_or_doctor,
    authorization_user,
    create_roles,
)
import pytest
from apps.core.management.commands.populate_users import (
    create_fake_users
)
from apps.core.management.commands.populate_clinics import (
    create_fake_clinics
)
from apps.core.management.commands.populate_doctor_specialties import (
    create_doctor_specialties
)


def save_fake_data() -> None:
    """
    Функция сохраняет в БД фековые данные для дальнейшего тестирования
    """
    doctors = create_fake_users('doctor', 5)
    specialties = [
        'Кардиолог',
        'Терапевт',
        'Хирург',
        'Невролог',
        'Офтальмолог'
    ]

    clinics = create_fake_clinics(3)
    create_doctor_specialties(doctors, clinics, specialties)


def get_consultation_data() -> dict:
    """
    Возвращает данные о тестовой записи на консультацию
    """
    consultation_data = {
        "doctor_in_clinics": 2,
        "start_time": "2025-03-05T11:46:53.435Z",
        "end_time": "2025-03-05T12:00:53.435Z",
        "status": "confirmed"
    }
    return consultation_data


def create_consultation() -> Any:
    """
    Функция создания тестовой записи (пациентом) на консультацию
    """
    create_roles()
    save_fake_data()
    _, payload_user_data = register_patient_or_doctor('patient')
    authorized_patient = authorization_user(
        payload_user_data['email'],
        payload_user_data['password']
    )
    get_access_token_and_pass_to_header(authorized_patient)
    response_create_consultation = client.post(
        '/api/v1/clinics/consultations/create/',
        get_consultation_data())
    client.credentials()
    return response_create_consultation


@pytest.mark.django_db
def test_create_consultation() -> None:
    """
    Тест создания записи на консультацию
    """
    response_create_consultation = create_consultation()
    assert response_create_consultation.status_code == 201
    assert response_create_consultation.data.get("id", None) is not None


def call_func_edite_consultation(
        data_to_update: dict,
        test_status="success") -> Any:

    """
    Функция создает запись о консультации
    для дальнешего теста на редактирование
    """
    created_consultation = create_consultation()
    if test_status == 'success':
        _, payload_user_data = register_patient_or_doctor('doctor')
        authorized_doctor = authorization_user(
            payload_user_data['email'],
            payload_user_data['password']
        )
        get_access_token_and_pass_to_header(authorized_doctor)
    data_to_update = data_to_update
    data_to_update["patient"] = 1
    data_to_update["end_time"] = "2025-04-05T12:00:53.435Z"
    response_update_consultation = client.put(
        f"/api/v1/clinics/consultations/update/"
        f"{created_consultation.data.get('id')}",
        data_to_update)
    client.credentials()
    return response_update_consultation


@pytest.mark.django_db
def test_unsuccessful_edite_consultation() -> None:
    """
    Тест на попытку редактирования записи
    неавторизированным пользователем
    """
    data_to_update = get_consultation_data()
    response = call_func_edite_consultation(
        data_to_update,
        'unsuccess'
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_successful_edite_consultation() -> None:
    """
    Тест на успешную попытку редактирования записи
    """
    data_to_update = get_consultation_data()
    response = call_func_edite_consultation(
        data_to_update,
        'success'
    )
    assert response.status_code == 200
    assert response.data['patient'] == 1
    assert response.data['end_time'] == "2025-04-05T12:00:53.435000Z"


def create_consultation_and_authorize_doctor() -> dict:
    """
    Функция создает запись на консультацию и авторизирует доктора,
    для дальнейшего тестирования доступа доктора к записям
    """
    consultation = create_consultation()
    _, payload_user_data = register_patient_or_doctor('doctor')
    authorized_doctor = authorization_user(
        payload_user_data['email'],
        payload_user_data['password']
    )
    get_access_token_and_pass_to_header(authorized_doctor)
    return consultation


def get_consultation_full_data_from_endpoint(role: str, conseltation_id: int):
    """
    Функция позволяет подключиться к ендпоинту от роли доктора или пользователя
    и получить полные данные о консультации
    """
    _, payload_user_data = register_patient_or_doctor(role)
    authorized_patient = authorization_user(
        payload_user_data['email'],
        payload_user_data['password']
    )
    get_access_token_and_pass_to_header(authorized_patient)
    response_get_consultation_data = client.get(
        f"/api/v1/clinics/consultations/{conseltation_id}"
    )
    client.credentials()
    return response_get_consultation_data


@pytest.mark.django_db
def test_get_full_consultation_data() -> None:
    """
    Тест получения полных данных о записи по id
    на консультацию.
    """
    create_roles()
    create_fake_users('patient', 2)
    save_fake_data()
    consultation = Consultation.objects.create(
        doctor_in_clinics=DoctorsSpecialityInClinics.objects.get(pk=6),
        start_time="2025-03-05T11:46:53.435Z",
        end_time="2025-03-05T12:00:53.435Z",
        status="confirmed",
        patient=Users.objects.get(pk=2)
    )
    (
        response_consultation_data_from_patient
    ) = get_consultation_full_data_from_endpoint(
        'patient', consultation.id)
    assert response_consultation_data_from_patient.status_code == 401
    (
        response_consultation_data_from_doctor
    ) = get_consultation_full_data_from_endpoint(
        'doctor', consultation.id
    )
    assert response_consultation_data_from_doctor.status_code == 200
    assert response_consultation_data_from_doctor.data.get(
        'id',
        None
    ) is not None


@pytest.mark.django_db
def test_delete_consultation() -> None:
    """
    Тест на успешное удаление записи о консультации
    """
    consultation = create_consultation_and_authorize_doctor()
    count_consultations_before_delete = Consultation.objects.all().count()
    response_delete_consultation = client.delete(
        f"/api/v1/clinics/consultations/{consultation.data['id']}/delete")
    client.credentials()
    assert response_delete_consultation.status_code == 204
    count_consultations_after_delete = Consultation.objects.all().count()
    assert (
        count_consultations_after_delete
    ) == count_consultations_before_delete - 1


@pytest.mark.django_db
def test_update_consultation_status() -> None:
    """
    Тест на смену статуса консультации
    """
    consultation = create_consultation_and_authorize_doctor()
    response_change_status = client.patch(
        f"/api/v1/clinics/consultations/{consultation.data['id']}"
        f"/change-status",
        {"status": "paid"}
    )
    client.credentials()
    assert response_change_status.status_code == 200
    assert response_change_status.data['status'] == 'paid'
