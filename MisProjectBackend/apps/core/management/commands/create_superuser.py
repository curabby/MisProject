from apps.core.models import Users


def create_superuser_handler():
    """
    Создание суперпользователя
    """
    try:
        Users.objects.create_superuser(
            email='admin@mail.com',
            password='admin',
            first_name='Admin',
            last_name='User',
            middle_name='Super',
        )
        print('Суперпользователь создан: admin@mail.com / admin')
    except Exception as e:
        print(f'Ошибка при создании суперпользователя: {e}')
