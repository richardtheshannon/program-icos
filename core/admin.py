from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "fellowship", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "fellowship")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Recovery", {"fields": ("sobriety_date", "fellowship")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Recovery", {"fields": ("sobriety_date", "fellowship")}),
    )
