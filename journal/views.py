import datetime

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from journal.forms import DailyInventoryForm, GratitudeEntryForm
from journal.models import DailyInventory, GratitudeEntry


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


class GratitudeView(View):
    """Today's gratitude list with inline add form."""

    def get(self, request: HttpRequest) -> HttpResponse:
        today = timezone.now().date()
        entries = GratitudeEntry.objects.filter(user=request.user, date=today)
        form = GratitudeEntryForm()
        return render(request, "journal/gratitude.html", {
            "entries": entries,
            "form": form,
            "gratitude_date": today,
        })


class GratitudeAddView(View):
    """HTMX POST: add a gratitude entry and return the updated list."""

    def post(self, request: HttpRequest) -> HttpResponse:
        today = timezone.now().date()
        form = GratitudeEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.date = today
            # Set order to next available
            max_order = (
                GratitudeEntry.objects.filter(user=request.user, date=today)
                .order_by("-order")
                .values_list("order", flat=True)
                .first()
            ) or 0
            entry.order = max_order + 1
            entry.save()
        # Return the full entry list partial for HTMX swap
        entries = GratitudeEntry.objects.filter(user=request.user, date=today)
        return render(request, "journal/partials/gratitude_list.html", {
            "entries": entries,
            "form": GratitudeEntryForm(),
        })


class GratitudeDeleteView(View):
    """HTMX DELETE: remove a gratitude entry and return the updated list."""

    def delete(self, request: HttpRequest, pk: str) -> HttpResponse:
        today = timezone.now().date()
        GratitudeEntry.objects.filter(pk=pk, user=request.user).delete()
        entries = GratitudeEntry.objects.filter(user=request.user, date=today)
        return render(request, "journal/partials/gratitude_list.html", {
            "entries": entries,
            "form": GratitudeEntryForm(),
        })


class GratitudeHistoryView(ListView):
    """Browse past gratitude entries grouped by date."""

    model = GratitudeEntry
    template_name = "journal/gratitude_history.html"
    context_object_name = "entries"
    paginate_by = 50

    def get_queryset(self):
        return (
            GratitudeEntry.objects.filter(user=self.request.user)
            .order_by("-date", "order")
        )

    def get_context_data(self, **kwargs: object) -> dict:
        context = super().get_context_data(**kwargs)
        # Group entries by date for display
        entries = context["entries"]
        grouped: dict[datetime.date, list[GratitudeEntry]] = {}
        for entry in entries:
            grouped.setdefault(entry.date, []).append(entry)
        context["grouped_entries"] = dict(sorted(grouped.items(), reverse=True))
        return context
