import json

from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from steps.forms import StepWorkForm
from steps.models import Question, Response, Step, StepProgress


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
    """Step detail page with question form. Handles GET (display) and POST (save)."""
    step = get_object_or_404(
        Step.objects.prefetch_related("questions"), number=step_number
    )

    # Get or create progress, mark as in_progress on first visit
    progress, created = StepProgress.objects.get_or_create(
        user=request.user, step=step
    )
    if progress.status == StepProgress.Status.NOT_STARTED:
        progress.status = StepProgress.Status.IN_PROGRESS
        progress.started_at = timezone.now()
        progress.save()

    # Previous / next step navigation
    prev_step = Step.objects.filter(number__lt=step.number).order_by("-number").first()
    next_step = Step.objects.filter(number__gt=step.number).order_by("number").first()

    if request.method == "POST":
        # Handle status change buttons
        new_status = request.POST.get("set_status")
        if new_status in ("complete", "revisiting"):
            progress.status = new_status
            if new_status == "complete":
                progress.completed_at = timezone.now()
            progress.save()
            label = "Complete" if new_status == "complete" else "Revisiting"
            messages.success(request, f"Step {step.number} marked as {label}.")
            return redirect("step_detail", step_number=step.number)

        # Handle form save
        form = StepWorkForm(request.POST, step=step, user=request.user)
        if form.is_valid():
            answered = form.save()
            messages.success(request, f"Progress saved — {answered} answers recorded.")
            return redirect("step_detail", step_number=step.number)
    else:
        form = StepWorkForm(step=step, user=request.user)

    # Build question-field pairs for template rendering
    questions = list(step.questions.all())
    question_fields = []
    for question in questions:
        field_name = f"q_{question.id}"
        question_fields.append({
            "question": question,
            "field": form[field_name],
            "field_name": field_name,
        })

    total_questions = len(questions)
    answered_count = Response.objects.filter(
        user=request.user, question__step=step
    ).exclude(answer="").count()
    percentage = int((answered_count / total_questions) * 100) if total_questions > 0 else 0

    return render(request, "steps/step_detail.html", {
        "step": step,
        "form": form,
        "question_fields": question_fields,
        "progress": progress,
        "prev_step": prev_step,
        "next_step": next_step,
        "total_questions": total_questions,
        "answered_count": answered_count,
        "percentage": percentage,
    })


@require_POST
def auto_save_response(request: HttpRequest) -> HttpResponse:
    """HTMX endpoint: auto-save a single question response."""
    question_id = request.POST.get("question_id")
    if not question_id:
        return JsonResponse({"error": "Missing question_id"}, status=400)

    question = get_object_or_404(Question, pk=question_id)
    field_name = f"q_{question_id}"
    answer = request.POST.get(field_name, "")

    Response.objects.update_or_create(
        user=request.user,
        question=question,
        defaults={"answer": answer},
    )

    # Update step progress if it was not_started
    progress, _ = StepProgress.objects.get_or_create(
        user=request.user, step=question.step
    )
    if progress.status == StepProgress.Status.NOT_STARTED:
        progress.status = StepProgress.Status.IN_PROGRESS
        progress.started_at = timezone.now()
        progress.save()

    return render(request, "steps/partials/save_indicator.html", {
        "saved": True,
        "question_id": question_id,
    })
