import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom user model with UUID primary key for PS01."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sobriety_date = models.DateField(null=True, blank=True)
    fellowship = models.CharField(max_length=50, default="AA")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def sobriety_days(self) -> int | None:
        """Returns number of days sober, or None if no sobriety date set."""
        if self.sobriety_date:
            return (timezone.now().date() - self.sobriety_date).days
        return None

    def __str__(self) -> str:
        return self.email or self.username
