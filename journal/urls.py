from django.urls import path

from journal.views import (
    DailyCheckinView,
    GratitudeAddView,
    GratitudeDeleteView,
    GratitudeHistoryView,
    GratitudeView,
    JournalExportView,
    JournalHistoryView,
    StreakView,
)

urlpatterns = [
    path("", DailyCheckinView.as_view(), name="daily_checkin"),
    path("history/", JournalHistoryView.as_view(), name="journal_history"),
    path("streak/", StreakView.as_view(), name="journal_streak"),
    path("gratitude/", GratitudeView.as_view(), name="gratitude"),
    path("gratitude/add/", GratitudeAddView.as_view(), name="gratitude_add"),
    path("gratitude/<uuid:pk>/delete/", GratitudeDeleteView.as_view(), name="gratitude_delete"),
    path("gratitude/history/", GratitudeHistoryView.as_view(), name="gratitude_history"),
    path("export/", JournalExportView.as_view(), name="journal_export"),
    path("<str:date>/", DailyCheckinView.as_view(), name="daily_checkin_date"),
]
