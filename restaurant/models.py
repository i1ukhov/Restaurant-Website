from django.db import models

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
