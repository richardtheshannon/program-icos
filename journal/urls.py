from django.urls import path

from journal.views import DailyCheckinView, JournalHistoryView, StreakView

urlpatterns = [
    path("", DailyCheckinView.as_view(), name="daily_checkin"),
    path("history/", JournalHistoryView.as_view(), name="journal_history"),
    path("streak/", StreakView.as_view(), name="journal_streak"),
    path("<str:date>/", DailyCheckinView.as_view(), name="daily_checkin_date"),
]
