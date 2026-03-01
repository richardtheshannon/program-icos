from django.contrib import admin

from amends.models import Amend, Person


class AmendInline(admin.TabularInline):
    model = Amend
    extra = 0


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "relationship", "willingness_level", "user")
    list_filter = ("willingness_level",)
    search_fields = ("name", "relationship")
    inlines = [AmendInline]


@admin.register(Amend)
class AmendAdmin(admin.ModelAdmin):
    list_display = ("person", "status", "updated_at")
    list_filter = ("status",)
