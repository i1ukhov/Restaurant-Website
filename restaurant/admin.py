from django.contrib import admin

from restaurant.models import Dish, Reservation


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "weight", "description", "price", "category")
    search_fields = ("id", "name", "weight", "description", "ingredients", "category")
    list_filter = ("category",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "table", "time", "status", "created_at", "user")
    search_fields = ("id", "date", "table", "time", "status", "created_at", "user")
    list_filter = ("date", "table", "time", "status", "created_at", "user")
