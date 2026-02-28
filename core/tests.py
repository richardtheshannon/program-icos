import datetime

import pytest
from django.utils import timezone

from core.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self) -> None:
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        assert user.email == "test@example.com"
        assert user.fellowship == "AA"
        assert user.sobriety_days() is None

    def test_sobriety_days(self) -> None:
        user = User.objects.create_user(
            username="soberuser",
            email="sober@example.com",
            password="testpass123",
            sobriety_date=timezone.now().date() - datetime.timedelta(days=30),
        )
        assert user.sobriety_days() == 30

    def test_str_returns_email(self) -> None:
        user = User.objects.create_user(
            username="struser",
            email="str@example.com",
            password="testpass123",
        )
        assert str(user) == "str@example.com"

    def test_uuid_primary_key(self) -> None:
        user = User.objects.create_user(
            username="uuiduser",
            email="uuid@example.com",
            password="testpass123",
        )
        assert user.pk is not None
        assert len(str(user.pk)) == 36  # UUID format


@pytest.mark.django_db
class TestSeedUserCommand:
    def test_seed_user_creates_superuser(self) -> None:
        from django.core.management import call_command
        from io import StringIO

        out = StringIO()
        call_command("seed_user", stdout=out)
        output = out.getvalue()

        # Should either create or skip (idempotent)
        assert "created" in output or "already exists" in output

    def test_seed_user_idempotent(self) -> None:
        from django.core.management import call_command
        from io import StringIO

        out1 = StringIO()
        call_command("seed_user", stdout=out1)

        out2 = StringIO()
        call_command("seed_user", stdout=out2)
        assert "already exists" in out2.getvalue()
