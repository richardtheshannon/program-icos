import datetime

import pytest
from django.test import Client
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


@pytest.mark.django_db
class TestMiddleware:
    def test_unauthenticated_redirects_to_login(self, client: Client) -> None:
        response = client.get("/dashboard/")
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_login_page_accessible_without_auth(self, client: Client) -> None:
        response = client.get("/login/")
        assert response.status_code == 200

    def test_admin_accessible_without_auth(self, client: Client) -> None:
        response = client.get("/admin/login/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestViews:
    def test_root_redirects_to_dashboard(self, client: Client) -> None:
        user = User.objects.create_user(username="viewuser", password="testpass123")
        client.force_login(user)
        response = client.get("/")
        assert response.status_code == 302
        assert response.url == "/dashboard/"

    def test_dashboard_requires_login(self, client: Client) -> None:
        response = client.get("/dashboard/")
        assert response.status_code == 302

    def test_dashboard_renders_for_authenticated_user(self, client: Client) -> None:
        user = User.objects.create_user(username="dashuser", password="testpass123")
        client.force_login(user)
        response = client.get("/dashboard/")
        assert response.status_code == 200
        assert b"Powerful Silence" in response.content

    def test_login_page_renders(self, client: Client) -> None:
        response = client.get("/login/")
        assert response.status_code == 200
        assert b"Sign In" in response.content

    def test_login_and_redirect(self, client: Client) -> None:
        User.objects.create_user(username="loginuser", password="testpass123")
        response = client.post("/login/", {"username": "loginuser", "password": "testpass123"})
        assert response.status_code == 302

    def test_logout_redirects_to_login(self, client: Client) -> None:
        user = User.objects.create_user(username="logoutuser", password="testpass123")
        client.force_login(user)
        response = client.post("/logout/")
        assert response.status_code == 302
