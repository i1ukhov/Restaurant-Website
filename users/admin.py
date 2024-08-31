from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "fullname", "phone")
    search_fields = ("id", "email", "fullname", "phone")
    list_filter = ("id", "email", "fullname", "phone")
