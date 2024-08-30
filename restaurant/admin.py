from django.contrib import admin

from restaurant.models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "weight", "description", "price", "category")
    search_fields = ("id", "name", "weight", "description", "ingredients", "category")
    list_filter = ("category",)
