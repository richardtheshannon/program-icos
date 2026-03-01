from django.contrib import admin

from journal.models import DailyInventory, GratitudeEntry


@admin.register(DailyInventory)
class DailyInventoryAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "serenity_level", "mood", "did_pray", "did_meditate")
    list_filter = ("date", "did_pray", "did_meditate")
    search_fields = ("user__username",)


@admin.register(GratitudeEntry)
class GratitudeEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "entry", "order")
    list_filter = ("date",)
    search_fields = ("user__username", "entry")
