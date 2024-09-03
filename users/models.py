from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите email"
    )

    fullname = models.CharField(
        max_length=100, verbose_name="Имя", help_text="Введите полное имя"
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        **NULLABLE,
        help_text="Введите номер телефона",
    )

    token = models.CharField(max_length=50, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"Клиент №{self.pk} – {self.fullname}. Email: {self.email}. Номер телефона: {self.phone if self.phone else 'не указан'}"
