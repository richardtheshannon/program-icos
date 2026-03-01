import datetime
from io import StringIO

import pytest
from django.core.management import call_command
from django.test import Client
from django.utils import timezone

from core.models import User
from steps.models import Question, Response, Step, StepProgress


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


@pytest.mark.django_db
class TestDashboardWithData:
    """Tests for the dashboard view with real step progress, sobriety, and activity data."""

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(
            username="dashdata",
            password="testpass123",
            email="dashdata@example.com",
        )

    @pytest.fixture
    def user_with_sobriety(self) -> User:
        return User.objects.create_user(
            username="soberdata",
            password="testpass123",
            sobriety_date=timezone.now().date() - datetime.timedelta(days=90),
        )

    @pytest.fixture
    def steps(self) -> list[Step]:
        """Create 3 steps with questions for testing."""
        created = []
        for i in range(1, 4):
            step = Step.objects.create(
                number=i,
                title=f"Step {i}",
                description=f"Description {i}",
                focus=f"Focus {i}",
                recovery_outcome=f"Outcome {i}",
                spiritual_principle=f"Principle {i}",
                order=i,
            )
            for q_num in range(1, 4):
                Question.objects.create(
                    step=step,
                    number=q_num,
                    text=f"Step {i} Question {q_num}?",
                )
            created.append(step)
        return created

    def test_dashboard_shows_step_progress(self, client: Client, user: User, steps: list[Step]) -> None:
        StepProgress.objects.create(user=user, step=steps[0], status=StepProgress.Status.COMPLETE)
        StepProgress.objects.create(user=user, step=steps[1], status=StepProgress.Status.IN_PROGRESS)
        client.force_login(user)
        response = client.get("/dashboard/")
        assert response.status_code == 200
        ctx = response.context
        assert ctx["steps_complete"] == 1
        assert len(ctx["step_statuses"]) == 3
        assert ctx["step_statuses"][0]["status"] == StepProgress.Status.COMPLETE
        assert ctx["step_statuses"][1]["status"] == StepProgress.Status.IN_PROGRESS

    def test_dashboard_current_step(self, client: Client, user: User, steps: list[Step]) -> None:
        StepProgress.objects.create(user=user, step=steps[0], status=StepProgress.Status.COMPLETE)
        client.force_login(user)
        response = client.get("/dashboard/")
        assert response.context["current_step"].number == 2

    def test_dashboard_overall_percentage(self, client: Client, user: User, steps: list[Step]) -> None:
        for step in steps:
            StepProgress.objects.create(user=user, step=step, status=StepProgress.Status.COMPLETE)
        client.force_login(user)
        response = client.get("/dashboard/")
        assert response.context["steps_complete"] == 3
        assert response.context["overall_percentage"] == 25  # 3/12 = 25%

    def test_dashboard_sobriety_breakdown(self, client: Client, user_with_sobriety: User) -> None:
        client.force_login(user_with_sobriety)
        response = client.get("/dashboard/")
        breakdown = response.context["sobriety_breakdown"]
        assert breakdown is not None
        assert breakdown["total_days"] == 90
        assert breakdown["months"] == 3

    def test_dashboard_no_sobriety_date(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/dashboard/")
        assert response.context["sobriety_breakdown"] is None

    def test_dashboard_recent_activity(self, client: Client, user: User, steps: list[Step]) -> None:
        q = steps[0].questions.first()
        Response.objects.create(user=user, question=q, answer="My answer")
        client.force_login(user)
        response = client.get("/dashboard/")
        recent = response.context["recent_responses"]
        assert len(recent) == 1
        assert recent[0].answer == "My answer"

    def test_dashboard_recent_activity_excludes_empty(self, client: Client, user: User, steps: list[Step]) -> None:
        q1 = steps[0].questions.first()
        q2 = steps[0].questions.last()
        Response.objects.create(user=user, question=q1, answer="Real answer")
        Response.objects.create(user=user, question=q2, answer="")
        client.force_login(user)
        response = client.get("/dashboard/")
        recent = response.context["recent_responses"]
        assert len(recent) == 1

    def test_dashboard_recent_activity_limited_to_5(self, client: Client, user: User, steps: list[Step]) -> None:
        for step in steps:
            for q in step.questions.all():
                Response.objects.create(user=user, question=q, answer=f"Answer for {q}")
        client.force_login(user)
        response = client.get("/dashboard/")
        assert len(response.context["recent_responses"]) == 5

    def test_dashboard_renders_step_circles(self, client: Client, user: User, steps: list[Step]) -> None:
        StepProgress.objects.create(user=user, step=steps[0], status=StepProgress.Status.COMPLETE)
        client.force_login(user)
        response = client.get("/dashboard/")
        content = response.content.decode()
        assert "Step Progress" in content
        assert "/steps/1/" in content

    def test_dashboard_renders_continue_button(self, client: Client, user: User, steps: list[Step]) -> None:
        StepProgress.objects.create(user=user, step=steps[0], status=StepProgress.Status.COMPLETE)
        client.force_login(user)
        response = client.get("/dashboard/")
        assert b"Continue Step 2" in response.content


@pytest.mark.django_db
class TestSetSobrietyDateView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="sobriety", password="testpass123")

    def test_set_sobriety_date(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.post("/dashboard/set-sobriety-date/", {"sobriety_date": "2024-01-15"})
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.sobriety_date == datetime.date(2024, 1, 15)

    def test_set_sobriety_date_empty(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.post("/dashboard/set-sobriety-date/", {"sobriety_date": ""})
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.sobriety_date is None

    def test_set_sobriety_date_future_rejected(self, client: Client, user: User) -> None:
        client.force_login(user)
        future = (timezone.now().date() + datetime.timedelta(days=10)).isoformat()
        response = client.post("/dashboard/set-sobriety-date/", {"sobriety_date": future})
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.sobriety_date is None

    def test_set_sobriety_date_invalid_format(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.post("/dashboard/set-sobriety-date/", {"sobriety_date": "not-a-date"})
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.sobriety_date is None


@pytest.mark.django_db
class TestAccessibility:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="a11yuser", password="testpass123")

    def test_skip_to_content_link(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/dashboard/")
        assert b"Skip to main content" in response.content
        assert b'id="main-content"' in response.content

    def test_sidebar_nav_aria_label(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/dashboard/")
        assert b'aria-label="Main navigation"' in response.content

    def test_sidebar_active_aria_current(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/dashboard/")
        assert b'aria-current="page"' in response.content

    def test_mobile_menu_aria_label(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/dashboard/")
        assert b'aria-label="Toggle navigation menu"' in response.content

    def test_step_detail_breadcrumb(self, client: Client, user: User) -> None:
        call_command("seed_steps", stdout=StringIO())
        client.force_login(user)
        response = client.get("/steps/1/")
        content = response.content.decode()
        assert 'aria-label="Breadcrumb"' in content
        assert "Step Work" in content
        assert 'aria-current="page"' in content
