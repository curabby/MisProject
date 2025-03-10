from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        """Создаёт обычного пользователя с указанной ролью."""
        if not email:
            raise ValueError('The Email field must be set')
        required_fields = ['first_name', 'last_name', 'middle_name']
        for field in required_fields:
            if field not in extra_fields:
                raise ValueError(f'The {field} field must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создаёт суперпользователя с ролью admin."""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        try:
            admin_role = Role.objects.get(name='admin')
        except Exception as err:
            return f"Возникла ошибка {err}"
        return self.create_user(
            email,
            password,
            role=admin_role,
            **extra_fields
        )


class Users(AbstractBaseUser, PermissionsMixin):
    '''
    Модель для хранения данных о пациентах
    '''
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    middle_name = models.CharField(max_length=128, blank=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
