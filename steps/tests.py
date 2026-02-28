from io import StringIO

import pytest
from django.core.management import call_command
from django.test import Client

from core.models import User
from steps.models import Question, Response, Step, StepProgress


@pytest.mark.django_db
class TestSeedSteps:
    def test_seed_creates_12_steps(self) -> None:
        call_command("seed_steps", stdout=StringIO())
        assert Step.objects.count() == 12

    def test_seed_creates_questions(self) -> None:
        call_command("seed_steps", stdout=StringIO())
        total = Question.objects.count()
        assert total >= 130  # ~136 original questions

    def test_recurring_steps(self) -> None:
        call_command("seed_steps", stdout=StringIO())
        recurring = Step.objects.filter(is_recurring=True).values_list("number", flat=True)
        assert set(recurring) == {10, 11, 12}

    def test_seed_is_idempotent(self) -> None:
        call_command("seed_steps", stdout=StringIO())
        call_command("seed_steps", stdout=StringIO())
        assert Step.objects.count() == 12

    def test_step_ordering(self) -> None:
        call_command("seed_steps", stdout=StringIO())
        numbers = list(Step.objects.values_list("number", flat=True))
        assert numbers == list(range(1, 13))


@pytest.mark.django_db
class TestStepModels:
    def test_step_str(self) -> None:
        step = Step.objects.create(
            number=99, title="Test Step", description="d",
            focus="f", recovery_outcome="r", spiritual_principle="Test",
        )
        assert str(step) == "Step 99: Test Step"

    def test_question_str(self) -> None:
        step = Step.objects.create(
            number=99, title="Test", description="d",
            focus="f", recovery_outcome="r", spiritual_principle="Test",
        )
        q = Question.objects.create(step=step, number=1, text="Test question?")
        assert str(q) == "Step 99, Q1"

    def test_completion_percentage_no_questions(self) -> None:
        user = User.objects.create_user(username="pctuser", password="pass123")
        step = Step.objects.create(
            number=99, title="Empty", description="d",
            focus="f", recovery_outcome="r", spiritual_principle="Test",
        )
        progress = StepProgress.objects.create(user=user, step=step)
        assert progress.completion_percentage() == 0

    def test_completion_percentage_with_answers(self) -> None:
        user = User.objects.create_user(username="ansuser", password="pass123")
        step = Step.objects.create(
            number=99, title="Pct", description="d",
            focus="f", recovery_outcome="r", spiritual_principle="Test",
        )
        q1 = Question.objects.create(step=step, number=1, text="Q1?")
        q2 = Question.objects.create(step=step, number=2, text="Q2?")
        Response.objects.create(user=user, question=q1, answer="answered")
        Response.objects.create(user=user, question=q2, answer="")  # blank = not answered
        progress = StepProgress.objects.create(user=user, step=step)
        assert progress.completion_percentage() == 50


@pytest.mark.django_db
class TestStepListView:
    def test_step_list_requires_login(self, client: Client) -> None:
        response = client.get("/steps/")
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_step_list_renders_for_authenticated_user(self, client: Client) -> None:
        call_command("seed_steps", stdout=StringIO())
        user = User.objects.create_user(username="stepuser", password="pass123")
        client.force_login(user)
        response = client.get("/steps/")
        assert response.status_code == 200
        assert b"My Step Work" in response.content

    def test_step_list_shows_all_12_steps(self, client: Client) -> None:
        call_command("seed_steps", stdout=StringIO())
        user = User.objects.create_user(username="all12user", password="pass123")
        client.force_login(user)
        response = client.get("/steps/")
        content = response.content.decode()
        assert "Admitting Powerlessness" in content
        assert "Carrying the Message" in content

    def test_step_list_creates_progress_records(self, client: Client) -> None:
        call_command("seed_steps", stdout=StringIO())
        user = User.objects.create_user(username="progressuser", password="pass123")
        client.force_login(user)
        client.get("/steps/")
        assert StepProgress.objects.filter(user=user).count() == 12

    def test_step_detail_placeholder_renders(self, client: Client) -> None:
        call_command("seed_steps", stdout=StringIO())
        user = User.objects.create_user(username="detailuser", password="pass123")
        client.force_login(user)
        response = client.get("/steps/1/")
        assert response.status_code == 200
        assert b"Admitting Powerlessness" in response.content

    def test_step_detail_404_for_invalid_step(self, client: Client) -> None:
        user = User.objects.create_user(username="404user", password="pass123")
        client.force_login(user)
        response = client.get("/steps/99/")
        assert response.status_code == 404
