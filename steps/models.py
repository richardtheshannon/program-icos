import uuid

from django.conf import settings
from django.db import models


class Step(models.Model):
    """One of the 12 steps. Seeded via management command."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    focus = models.TextField()
    recovery_outcome = models.TextField()
    spiritual_principle = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_recurring = models.BooleanField(default=False)

    class Meta:
        ordering = ["number"]

    def __str__(self) -> str:
        return f"Step {self.number}: {self.title}"


class Question(models.Model):
    """A guided question within a step. Seeded via management command."""

    class QuestionType(models.TextChoices):
        TEXT = "text", "Open-ended text"
        YESNO_ELABORATE = "yesno", "Yes/No + Elaborate"
        LIST_BUILDER = "list", "List builder"
        LETTER = "letter", "Letter writing"
        ACTION_PLAN = "action", "Action planning"
        DAILY = "daily", "Daily recurring"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="questions")
    number = models.PositiveIntegerField()
    text = models.TextField()
    help_text = models.TextField(blank=True)
    question_type = models.CharField(
        max_length=10,
        choices=QuestionType.choices,
        default=QuestionType.TEXT,
    )
    is_required = models.BooleanField(default=False)

    class Meta:
        ordering = ["step__number", "number"]
        unique_together = ["step", "number"]

    def __str__(self) -> str:
        return f"Step {self.step.number}, Q{self.number}"


class Response(models.Model):
    """A user's answer to a question. One response per user per question."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="responses"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="responses"
    )
    answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "question"]

    def __str__(self) -> str:
        return f"{self.user} — {self.question}"


class StepProgress(models.Model):
    """Tracks a user's progress on a specific step."""

    class Status(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETE = "complete", "Complete"
        REVISITING = "revisiting", "Revisiting"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="step_progress"
    )
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="progress")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NOT_STARTED
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "step"]
        ordering = ["step__number"]

    def __str__(self) -> str:
        return f"{self.user} — Step {self.step.number}: {self.status}"

    def completion_percentage(self) -> int:
        """Calculate % of questions answered for this step."""
        total = self.step.questions.count()
        if total == 0:
            return 0
        answered = Response.objects.filter(
            user=self.user, question__step=self.step
        ).exclude(answer="").count()
        return int((answered / total) * 100)
