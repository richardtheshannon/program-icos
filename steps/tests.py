from io import StringIO

import pytest
from django.core.management import call_command
from django.test import Client

from core.models import User
from steps.forms import StepWorkForm
from steps.models import Question, Response, Step, StepProgress


# ---------------------------------------------------------------------------
# PDF export tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestStepExportView:
    def _setup(self, client: Client):
        call_command("seed_steps", stdout=StringIO())
        user = User.objects.create_user(username="exportuser", password="pass123")
        client.force_login(user)
        return user

    def test_export_requires_login(self, client: Client) -> None:
        call_command("seed_steps", stdout=StringIO())
        response = client.get("/steps/1/export/")
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_export_single_step_pdf(self, client: Client) -> None:
        self._setup(client)
        response = client.get("/steps/1/export/")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"
        assert 'step_1.pdf' in response["Content-Disposition"]

    def test_export_step_with_answers(self, client: Client) -> None:
        user = self._setup(client)
        step = Step.objects.get(number=1)
        q = step.questions.first()
        Response.objects.create(user=user, question=q, answer="My PDF answer")
        response = client.get("/steps/1/export/")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"

    def test_export_invalid_step_404(self, client: Client) -> None:
        self._setup(client)
        response = client.get("/steps/99/export/")
        assert response.status_code == 404

    def test_export_all_steps_pdf(self, client: Client) -> None:
        self._setup(client)
        response = client.get("/steps/export/all/")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"
        assert 'all_steps.pdf' in response["Content-Disposition"]

    def test_export_all_requires_login(self, client: Client) -> None:
        response = client.get("/steps/export/all/")
        assert response.status_code == 302
        assert "/login/" in response.url


# ---------------------------------------------------------------------------
# Seed command tests
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Step list view tests
# ---------------------------------------------------------------------------

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

    def test_step_detail_renders(self, client: Client) -> None:
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


# ---------------------------------------------------------------------------
# Step detail view & form tests (Phase 5)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestStepDetailView:
    def _setup(self, client: Client):
        """Seed steps and log in a user."""
        call_command("seed_steps", stdout=StringIO())
        user = User.objects.create_user(username="formuser", password="pass123")
        client.force_login(user)
        return user

    def test_step_detail_requires_login(self, client: Client) -> None:
        call_command("seed_steps", stdout=StringIO())
        response = client.get("/steps/1/")
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_step_detail_shows_questions(self, client: Client) -> None:
        self._setup(client)
        response = client.get("/steps/1/")
        assert response.status_code == 200
        content = response.content.decode()
        assert "Save Progress" in content
        assert 'name="q_' in content

    def test_step_detail_sets_progress_to_in_progress(self, client: Client) -> None:
        user = self._setup(client)
        client.get("/steps/1/")
        step = Step.objects.get(number=1)
        progress = StepProgress.objects.get(user=user, step=step)
        assert progress.status == StepProgress.Status.IN_PROGRESS
        assert progress.started_at is not None

    def test_step_detail_navigation(self, client: Client) -> None:
        self._setup(client)
        response = client.get("/steps/1/")
        content = response.content.decode()
        assert "Step 2" in content
        assert "All Steps" in content

    def test_step_detail_save_answers(self, client: Client) -> None:
        user = self._setup(client)
        step = Step.objects.get(number=1)
        questions = list(step.questions.all()[:3])
        post_data = {}
        for q in questions:
            post_data[f"q_{q.id}"] = f"Answer for question {q.number}"
        response = client.post("/steps/1/", post_data)
        assert response.status_code == 302
        for q in questions:
            resp = Response.objects.get(user=user, question=q)
            assert resp.answer == f"Answer for question {q.number}"

    def test_step_detail_prepopulates_answers(self, client: Client) -> None:
        user = self._setup(client)
        step = Step.objects.get(number=1)
        q = step.questions.first()
        Response.objects.create(user=user, question=q, answer="My previous answer")
        response = client.get("/steps/1/")
        assert b"My previous answer" in response.content

    def test_mark_step_complete(self, client: Client) -> None:
        user = self._setup(client)
        step = Step.objects.get(number=1)
        response = client.post("/steps/1/", {"set_status": "complete"})
        assert response.status_code == 302
        progress = StepProgress.objects.get(user=user, step=step)
        assert progress.status == StepProgress.Status.COMPLETE
        assert progress.completed_at is not None

    def test_mark_step_revisiting(self, client: Client) -> None:
        user = self._setup(client)
        step = Step.objects.get(number=1)
        StepProgress.objects.filter(user=user, step=step).update(
            status=StepProgress.Status.COMPLETE
        )
        response = client.post("/steps/1/", {"set_status": "revisiting"})
        assert response.status_code == 302
        progress = StepProgress.objects.get(user=user, step=step)
        assert progress.status == StepProgress.Status.REVISITING


# ---------------------------------------------------------------------------
# StepWorkForm tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestStepWorkForm:
    def test_form_creates_fields_for_questions(self) -> None:
        step = Step.objects.create(
            number=99, title="Form Test", description="d",
            focus="f", recovery_outcome="r", spiritual_principle="Test",
        )
        q1 = Question.objects.create(step=step, number=1, text="Q1?")
        q2 = Question.objects.create(step=step, number=2, text="Q2?")
        user = User.objects.create_user(username="formuser2", password="pass123")
        form = StepWorkForm(step=step, user=user)
        assert f"q_{q1.id}" in form.fields
        assert f"q_{q2.id}" in form.fields

    def test_form_prepopulates_existing_answers(self) -> None:
        step = Step.objects.create(
            number=99, title="Prepop Test", description="d",
            focus="f", recovery_outcome="r", spiritual_principle="Test",
        )
        q = Question.objects.create(step=step, number=1, text="Q1?")
        user = User.objects.create_user(username="prepopuser", password="pass123")
        Response.objects.create(user=user, question=q, answer="existing answer")
        form = StepWorkForm(step=step, user=user)
        assert form.fields[f"q_{q.id}"].initial == "existing answer"

    def test_form_save_creates_responses(self) -> None:
        step = Step.objects.create(
            number=99, title="Save Test", description="d",
            focus="f", recovery_outcome="r", spiritual_principle="Test",
        )
        q = Question.objects.create(step=step, number=1, text="Q1?")
        user = User.objects.create_user(username="saveuser", password="pass123")
        form = StepWorkForm(
            data={f"q_{q.id}": "my answer"},
            step=step, user=user,
        )
        assert form.is_valid()
        answered = form.save()
        assert answered == 1
        assert Response.objects.get(user=user, question=q).answer == "my answer"


# ---------------------------------------------------------------------------
# Auto-save endpoint tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestAutoSave:
    def test_auto_save_requires_post(self, client: Client) -> None:
        user = User.objects.create_user(username="autouser", password="pass123")
        client.force_login(user)
        response = client.get("/steps/auto-save/")
        assert response.status_code == 405

    def test_auto_save_saves_response(self, client: Client) -> None:
        call_command("seed_steps", stdout=StringIO())
        user = User.objects.create_user(username="autosaveuser", password="pass123")
        client.force_login(user)
        step = Step.objects.get(number=1)
        q = step.questions.first()
        response = client.post("/steps/auto-save/", {
            "question_id": str(q.id),
            f"q_{q.id}": "auto saved answer",
        })
        assert response.status_code == 200
        assert b"Saved" in response.content
        saved = Response.objects.get(user=user, question=q)
        assert saved.answer == "auto saved answer"

    def test_auto_save_missing_question_id(self, client: Client) -> None:
        user = User.objects.create_user(username="missingq", password="pass123")
        client.force_login(user)
        response = client.post("/steps/auto-save/", {})
        assert response.status_code == 400
