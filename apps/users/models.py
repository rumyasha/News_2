from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Кастомный менеджер пользователей с email вместо username"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""

    username = None  # Удаляем username
    email = models.EmailField(_('email address'), unique=True)  # Делаем email уникальным

    USERNAME_FIELD = 'email'  # Используем email для входа
    REQUIRED_FIELDS = []  # Дополнительные поля при createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email