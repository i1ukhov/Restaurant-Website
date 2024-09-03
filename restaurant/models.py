from django.db import models
from multiselectfield import MultiSelectField

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Dish(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название блюда", help_text="Введите название блюда")
    photo = models.ImageField(upload_to="restaurant/images", verbose_name="Фото",
                              help_text="Загрузите фотографию блюда", **NULLABLE)
    description = models.TextField(verbose_name="Описание блюда", help_text="Введите описание блюда", **NULLABLE)
    ingredients = models.TextField(verbose_name="Состав", help_text="Введите состав блюда", **NULLABLE)
    weight = models.PositiveIntegerField(verbose_name="Вес блюда", help_text="Укажите вес блюда в граммах")
    price = models.PositiveIntegerField(verbose_name="Цена", help_text="Укажите цену блюда в рублях")
    category_choices = [
        ("appetisers", "Закуски"),
        ("breakfasts", "Завтраки"),
        ("salads", "Салаты"),
        ("cold side dish", "Холодные блюда"),
        ("hot side dish", "Горячие блюда"),
        ("desserts", "Десерты"),
        ("drinks", "Напитки"),
        ("extra", "Дополнительно"),
    ]
    category = models.CharField(max_length=25, choices=category_choices, verbose_name="Категория",
                                help_text="Выберите категорию")

    def __str__(self):
        return f"{self.name}. Вес: {self.weight} г. Стоимость: {self.price}"

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент", help_text="Укажите клиента", **NULLABLE)
    date = models.DateField(verbose_name="Дата бронирования", help_text="Укажите дату бронирования")
    table_choices = [
        ("1A", "№1 веранда"),
        ("2A", "№2 веранда"),
        ("3A", "№3 веранда"),
        ("4A", "№4 веранда"),
        ("5A", "№5 веранда"),
        ("6A", "№6 веранда"),
        ("1B", "№1 зал"),
        ("2B", "№2 зал"),
        ("3B", "№3 зал"),
        ("4B", "№4 зал"),
        ("5B", "№5 зал"),
        ("6B", "№6 зал"),
        ("7B", "№7 зал"),
        ("8B", "№8 зал"),
        ("9B", "№9 зал"),
        ("10B", "№10 зал"),
    ]
    table = models.CharField(max_length=5, choices=table_choices, verbose_name="Столик", help_text="Выберите столик")

    time_choices = [
        ("9", "9:00 - 10:00"),
        ("10", "10:00 - 11:00"),
        ("11", "11:00 - 12:00"),
        ("12", "12:00 - 13:00"),
        ("13", "13:00 - 14:00"),
        ("14", "14:00 - 15:00"),
        ("15", "15:00 - 16:00"),
        ("16", "16:00 - 17:00"),
        ("17", "17:00 - 18:00"),
        ("18", "18:00 - 19:00"),
        ("19", "19:00 - 20:00"),
        ("20", "20:00 - 21:00"),
        ("21", "21:00 - 22:00"),
        ("22", "22:00 - 23:00"),
    ]
    time = MultiSelectField(choices=time_choices, max_choices=4, verbose_name="Время", help_text="Выберите слоты по времени (до 4-х слотов)")

    status_choices = [
        ("created", "Создана"),
        ("confirmed", "Подтверждена"),
        ("completed", "Завершена"),
        ("canceled", "Отменена"),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default="created",
                              verbose_name="Статус бронирования", help_text="Укажите статус бронирования")

    created_at = models.DateTimeField(auto_now_add=True)

    reservation_token = models.CharField(max_length=50, verbose_name="Reservation token", **NULLABLE)

    def __str__(self):
        return f"Бронь №{self.pk} на {self.date}. Столик - {self.table}. Время: {self.time}"

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
