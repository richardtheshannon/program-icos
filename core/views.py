import datetime

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from journal.models import DailyInventory, GratitudeEntry
from steps.models import Response, Step, StepProgress


class DashboardView(TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs: object) -> dict:
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Step progress data
        steps = Step.objects.all()
        progress_records = StepProgress.objects.filter(user=user).select_related("step")
        progress_map = {sp.step.number: sp for sp in progress_records}

        steps_complete = sum(
            1 for sp in progress_records if sp.status == StepProgress.Status.COMPLETE
        )
        overall_percentage = int((steps_complete / 12) * 100) if steps else 0

        # Build per-step info for the visual
        step_statuses = []
        current_step = None
        for step in steps:
            sp = progress_map.get(step.number)
            status = sp.status if sp else StepProgress.Status.NOT_STARTED
            pct = sp.completion_percentage() if sp else 0
            step_statuses.append({
                "number": step.number,
                "title": step.title,
                "status": status,
                "percentage": pct,
            })
            if current_step is None and status != StepProgress.Status.COMPLETE:
                current_step = step

        # Sobriety breakdown
        sobriety_breakdown = None
        if user.sobriety_date:
            total_days = user.sobriety_days()
            if total_days is not None:
                years = total_days // 365
                remaining = total_days % 365
                months = remaining // 30
                days = remaining % 30
                sobriety_breakdown = {
                    "total_days": total_days,
                    "years": years,
                    "months": months,
                    "days": days,
                }

        # Recent activity — last 5 saved answers
        recent_responses = (
            Response.objects.filter(user=user)
            .exclude(answer="")
            .select_related("question__step")
            .order_by("-updated_at")[:5]
        )

        # Daily check-in status
        today = timezone.now().date()
        todays_checkin = DailyInventory.objects.filter(user=user, date=today).first()
        checkin_streak = DailyInventory.current_streak(user)

        # Gratitude count for today
        gratitude_count = GratitudeEntry.objects.filter(user=user, date=today).count()

        context.update({
            "steps_complete": steps_complete,
            "overall_percentage": overall_percentage,
            "step_statuses": step_statuses,
            "current_step": current_step,
            "sobriety_breakdown": sobriety_breakdown,
            "recent_responses": recent_responses,
            "today": today,
            "todays_checkin": todays_checkin,
            "checkin_streak": checkin_streak,
            "gratitude_count": gratitude_count,
        })
        return context


class PS01LoginView(LoginView):
    template_name = "core/login.html"
    redirect_authenticated_user = True


class PS01LogoutView(LogoutView):
    pass


class SetSobrietyDateView(View):
    """HTMX endpoint to set the user's sobriety date."""

    def post(self, request: HttpRequest) -> HttpResponse:
        date_str = request.POST.get("sobriety_date", "").strip()
        if not date_str:
            messages.error(request, "Please enter a valid date.")
            return redirect("dashboard")

        try:
            sobriety_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect("dashboard")

        if sobriety_date > timezone.now().date():
            messages.error(request, "Sobriety date cannot be in the future.")
            return redirect("dashboard")

        request.user.sobriety_date = sobriety_date
        request.user.save(update_fields=["sobriety_date"])
        messages.success(request, "Sobriety date saved.")
        return redirect("dashboard")


def root_redirect(request: HttpRequest) -> HttpResponse:
    return redirect("dashboard")
