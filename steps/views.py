from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from steps.models import Response, Step, StepProgress


class StepListView(ListView):
    """Shows all 12 steps with per-user progress indicators."""

    model = Step
    template_name = "steps/step_list.html"
    context_object_name = "steps"

    def get_queryset(self) -> QuerySet[Step]:
        return Step.objects.prefetch_related("questions").all()

    def get_context_data(self, **kwargs: object) -> dict:
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Find first incomplete step number
        current_step_found = False

        # Build progress data for each step
        progress_map: dict = {}
        for step in context["steps"]:
            progress, _ = StepProgress.objects.get_or_create(
                user=user, step=step
            )
            total_questions = step.questions.count()
            answered = Response.objects.filter(
                user=user, question__step=step
            ).exclude(answer="").count()
            pct = int((answered / total_questions) * 100) if total_questions > 0 else 0

            is_current = False
            if not current_step_found and progress.status != StepProgress.Status.COMPLETE:
                is_current = True
                current_step_found = True

            progress_map[step.pk] = {
                "progress": progress,
                "total_questions": total_questions,
                "answered": answered,
                "percentage": pct,
                "is_current": is_current,
            }

        context["progress_map"] = progress_map
        return context


def step_detail_view(request: HttpRequest, step_number: int) -> HttpResponse:
    """Placeholder for Phase 5 — individual step detail/form view."""
    step = get_object_or_404(Step, number=step_number)
    return render(request, "steps/step_detail_placeholder.html", {"step": step})
