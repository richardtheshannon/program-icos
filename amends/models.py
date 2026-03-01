import uuid

from django.conf import settings
from django.db import models


class Person(models.Model):
    """A person on the user's Step 8 amends list."""

    class Willingness(models.IntegerChoices):
        NOT_WILLING = 1, "Not willing"
        SOMEWHAT = 2, "Somewhat willing"
        WILLING = 3, "Willing"
        VERY_WILLING = 4, "Very willing"
        READY = 5, "Ready now"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="amends_people"
    )
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=200, blank=True)
    how_harmed = models.TextField(help_text="How did you harm this person?")
    willingness_level = models.IntegerField(
        choices=Willingness.choices, default=Willingness.WILLING
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.relationship})" if self.relationship else self.name

    def latest_amend(self) -> "Amend | None":
        return self.amends.order_by("-created_at").first()

    def current_status(self) -> str:
        amend = self.latest_amend()
        return amend.status if amend else Amend.Status.NOT_STARTED


class Amend(models.Model):
    """Tracks the Step 9 amend process for a specific person."""

    class Status(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        LETTER_DRAFTED = "letter_drafted", "Letter Drafted"
        DISCUSSED = "discussed", "Discussed with Sponsor"
        AMEND_MADE = "amend_made", "Amend Made"
        ONGOING = "ongoing", "Ongoing / Living Amend"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="amends")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NOT_STARTED
    )
    anger_letter = models.TextField(blank=True, help_text="Private anger letter — DO NOT SEND")
    apology_letter = models.TextField(blank=True, help_text="Apology / amends letter")
    actionable_amends = models.TextField(blank=True, help_text="Concrete actions to make amends")
    sponsor_feedback = models.TextField(blank=True, help_text="Feedback from your sponsor")
    post_amend_reflection = models.TextField(blank=True, help_text="How did making the amend feel?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Amend for {self.person.name} — {self.get_status_display()}"
