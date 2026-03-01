import datetime
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class DailyInventory(models.Model):
    """Daily Step 10/11 inventory and reflection."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="daily_inventories"
    )
    date = models.DateField()

    # Step 10 — Personal inventory
    serenity_level = models.PositiveIntegerField(
        default=5, help_text="Serenity level 1-10"
    )
    was_resentful = models.BooleanField(default=False)
    resentful_details = models.TextField(blank=True)
    was_selfish = models.BooleanField(default=False)
    selfish_details = models.TextField(blank=True)
    was_dishonest = models.BooleanField(default=False)
    dishonest_details = models.TextField(blank=True)

    # Step 11 — Prayer and meditation
    did_pray = models.BooleanField(default=False)
    did_meditate = models.BooleanField(default=False)
    spiritual_notes = models.TextField(blank=True)

    # General
    mood = models.PositiveIntegerField(default=5, help_text="Mood level 1-10")
    additional_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "date"]
        ordering = ["-date"]
        verbose_name_plural = "daily inventories"

    def __str__(self) -> str:
        return f"{self.user} — {self.date}"

    @classmethod
    def current_streak(cls, user: settings.AUTH_USER_MODEL) -> int:
        """Calculate consecutive days of check-ins ending today or yesterday."""
        today = timezone.now().date()
        dates = list(
            cls.objects.filter(user=user, date__lte=today)
            .order_by("-date")
            .values_list("date", flat=True)
        )
        if not dates:
            return 0

        streak = 0
        expected = today
        # Allow streak to start from today or yesterday
        if dates[0] == today:
            expected = today
        elif dates[0] == today - datetime.timedelta(days=1):
            expected = today - datetime.timedelta(days=1)
        else:
            return 0

        for d in dates:
            if d == expected:
                streak += 1
                expected -= datetime.timedelta(days=1)
            else:
                break
        return streak


class GratitudeEntry(models.Model):
    """A single gratitude entry for a given day."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="gratitude_entries"
    )
    date = models.DateField()
    entry = models.TextField()
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "order"]
        verbose_name_plural = "gratitude entries"

    def __str__(self) -> str:
        return f"{self.user} — {self.date}: {self.entry[:50]}"
