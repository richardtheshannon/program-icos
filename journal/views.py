import datetime

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from journal.forms import DailyInventoryForm
from journal.models import DailyInventory


class DailyCheckinView(View):
    """GET: show today's (or a specific date's) check-in form. POST: save it."""

    def get(self, request: HttpRequest, date: str | None = None) -> HttpResponse:
        checkin_date = self._parse_date(date)
        inventory = DailyInventory.objects.filter(
            user=request.user, date=checkin_date
        ).first()
        form = DailyInventoryForm(instance=inventory)
        streak = DailyInventory.current_streak(request.user)
        return render(request, "journal/daily_checkin.html", {
            "form": form,
            "checkin_date": checkin_date,
            "is_today": checkin_date == timezone.now().date(),
            "inventory": inventory,
            "streak": streak,
        })

    def post(self, request: HttpRequest, date: str | None = None) -> HttpResponse:
        checkin_date = self._parse_date(date)
        inventory = DailyInventory.objects.filter(
            user=request.user, date=checkin_date
        ).first()
        form = DailyInventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.date = checkin_date
            obj.save()
            messages.success(request, f"Check-in for {checkin_date} saved.")
            return redirect("daily_checkin")
        streak = DailyInventory.current_streak(request.user)
        return render(request, "journal/daily_checkin.html", {
            "form": form,
            "checkin_date": checkin_date,
            "is_today": checkin_date == timezone.now().date(),
            "inventory": inventory,
            "streak": streak,
        })

    def _parse_date(self, date_str: str | None) -> datetime.date:
        if date_str:
            try:
                return datetime.date.fromisoformat(date_str)
            except ValueError:
                pass
        return timezone.now().date()


class JournalHistoryView(ListView):
    """Paginated list of past daily inventories."""

    model = DailyInventory
    template_name = "journal/history.html"
    context_object_name = "entries"
    paginate_by = 14

    def get_queryset(self):
        return DailyInventory.objects.filter(user=self.request.user)


class StreakView(View):
    """HTMX partial returning the current streak count."""

    def get(self, request: HttpRequest) -> HttpResponse:
        streak = DailyInventory.current_streak(request.user)
        return render(request, "journal/partials/streak_widget.html", {
            "streak": streak,
        })
