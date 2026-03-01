import datetime

import pytest
from django.test import Client
from django.utils import timezone

from core.models import User
from journal.models import DailyInventory, GratitudeEntry


# ---------------------------------------------------------------------------
# Journal export tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestJournalExportView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="exportjrnl", password="testpass123")

    def test_export_requires_login(self, client: Client) -> None:
        response = client.get("/journal/export/")
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_export_pdf_empty(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/journal/export/")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"
        assert 'journal_export.pdf' in response["Content-Disposition"]

    def test_export_pdf_with_entries(self, client: Client, user: User) -> None:
        today = timezone.now().date()
        DailyInventory.objects.create(
            user=user, date=today, serenity_level=8, mood=7,
            was_resentful=True, resentful_details="Felt angry at traffic"
        )
        client.force_login(user)
        response = client.get("/journal/export/")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"

    def test_export_pdf_custom_date_range(self, client: Client, user: User) -> None:
        DailyInventory.objects.create(
            user=user, date=datetime.date(2024, 6, 15), serenity_level=5, mood=6
        )
        client.force_login(user)
        response = client.get("/journal/export/?start=2024-06-01&end=2024-06-30")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"

    def test_export_pdf_invalid_dates_fallback(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/journal/export/?start=bad&end=bad")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"


@pytest.mark.django_db
class TestDailyInventoryModel:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="journaluser", password="testpass123")

    def test_create_inventory(self, user: User) -> None:
        inv = DailyInventory.objects.create(
            user=user, date=timezone.now().date(), serenity_level=7, mood=8
        )
        assert inv.serenity_level == 7
        assert inv.mood == 8
        assert inv.was_resentful is False

    def test_unique_per_user_per_date(self, user: User) -> None:
        today = timezone.now().date()
        DailyInventory.objects.create(user=user, date=today)
        with pytest.raises(Exception):
            DailyInventory.objects.create(user=user, date=today)

    def test_str(self, user: User) -> None:
        inv = DailyInventory.objects.create(user=user, date=datetime.date(2024, 6, 15))
        assert "2024-06-15" in str(inv)


@pytest.mark.django_db
class TestStreakCalculation:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="streakuser", password="testpass123")

    def test_no_entries_returns_zero(self, user: User) -> None:
        assert DailyInventory.current_streak(user) == 0

    def test_today_only(self, user: User) -> None:
        DailyInventory.objects.create(user=user, date=timezone.now().date())
        assert DailyInventory.current_streak(user) == 1

    def test_consecutive_days(self, user: User) -> None:
        today = timezone.now().date()
        for i in range(5):
            DailyInventory.objects.create(user=user, date=today - datetime.timedelta(days=i))
        assert DailyInventory.current_streak(user) == 5

    def test_gap_breaks_streak(self, user: User) -> None:
        today = timezone.now().date()
        DailyInventory.objects.create(user=user, date=today)
        DailyInventory.objects.create(user=user, date=today - datetime.timedelta(days=1))
        # Skip day 2, add day 3
        DailyInventory.objects.create(user=user, date=today - datetime.timedelta(days=3))
        assert DailyInventory.current_streak(user) == 2

    def test_yesterday_starts_streak(self, user: User) -> None:
        today = timezone.now().date()
        DailyInventory.objects.create(user=user, date=today - datetime.timedelta(days=1))
        DailyInventory.objects.create(user=user, date=today - datetime.timedelta(days=2))
        assert DailyInventory.current_streak(user) == 2

    def test_old_entry_no_streak(self, user: User) -> None:
        DailyInventory.objects.create(
            user=user, date=timezone.now().date() - datetime.timedelta(days=10)
        )
        assert DailyInventory.current_streak(user) == 0


@pytest.mark.django_db
class TestGratitudeEntryModel:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="gratuser", password="testpass123")

    def test_create_entry(self, user: User) -> None:
        entry = GratitudeEntry.objects.create(
            user=user, date=timezone.now().date(), entry="Grateful for sunlight"
        )
        assert "Grateful for sunlight" in str(entry)


@pytest.mark.django_db
class TestDailyCheckinView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="checkinview", password="testpass123")

    def test_checkin_requires_login(self, client: Client) -> None:
        response = client.get("/journal/")
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_checkin_get_empty(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/journal/")
        assert response.status_code == 200
        assert b"Step 10" in response.content

    def test_checkin_post_creates_inventory(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.post("/journal/", {
            "serenity_level": "7",
            "mood": "8",
            "was_resentful": "",
            "was_selfish": "",
            "was_dishonest": "",
        })
        assert response.status_code == 302
        assert DailyInventory.objects.filter(user=user).count() == 1
        inv = DailyInventory.objects.get(user=user)
        assert inv.serenity_level == 7
        assert inv.mood == 8

    def test_checkin_prepopulates_existing(self, client: Client, user: User) -> None:
        today = timezone.now().date()
        DailyInventory.objects.create(
            user=user, date=today, serenity_level=3, mood=4,
            was_resentful=True, resentful_details="Test resentment"
        )
        client.force_login(user)
        response = client.get("/journal/")
        assert response.status_code == 200
        assert b"Test resentment" in response.content

    def test_checkin_specific_date(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/journal/2024-06-15/")
        assert response.status_code == 200

    def test_checkin_post_updates_existing(self, client: Client, user: User) -> None:
        today = timezone.now().date()
        DailyInventory.objects.create(user=user, date=today, serenity_level=3, mood=4)
        client.force_login(user)
        response = client.post("/journal/", {
            "serenity_level": "9",
            "mood": "10",
        })
        assert response.status_code == 302
        inv = DailyInventory.objects.get(user=user, date=today)
        assert inv.serenity_level == 9


@pytest.mark.django_db
class TestJournalHistoryView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="historyuser", password="testpass123")

    def test_history_requires_login(self, client: Client) -> None:
        response = client.get("/journal/history/")
        assert response.status_code == 302

    def test_history_shows_entries(self, client: Client, user: User) -> None:
        DailyInventory.objects.create(user=user, date=datetime.date(2024, 6, 15))
        client.force_login(user)
        response = client.get("/journal/history/")
        assert response.status_code == 200
        assert b"June 15, 2024" in response.content

    def test_history_empty_state(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/journal/history/")
        assert response.status_code == 200
        assert b"No check-ins yet" in response.content


@pytest.mark.django_db
class TestDashboardCheckinWidget:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="dashcheckin", password="testpass123")

    def test_dashboard_shows_checkin_not_complete(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/dashboard/")
        assert b"Not yet completed" in response.content

    def test_dashboard_shows_checkin_complete(self, client: Client, user: User) -> None:
        DailyInventory.objects.create(
            user=user, date=timezone.now().date(), serenity_level=7, mood=8
        )
        client.force_login(user)
        response = client.get("/dashboard/")
        assert b"Complete" in response.content
        assert b"Serenity: 7/10" in response.content


@pytest.mark.django_db
class TestGratitudeView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="gratview", password="testpass123")

    def test_gratitude_requires_login(self, client: Client) -> None:
        response = client.get("/journal/gratitude/")
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_gratitude_page_renders(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/journal/gratitude/")
        assert response.status_code == 200
        assert b"What are you grateful for today?" in response.content

    def test_gratitude_shows_entries(self, client: Client, user: User) -> None:
        today = timezone.now().date()
        GratitudeEntry.objects.create(user=user, date=today, entry="Sunshine", order=1)
        client.force_login(user)
        response = client.get("/journal/gratitude/")
        assert b"Sunshine" in response.content

    def test_gratitude_empty_state(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/journal/gratitude/")
        assert b"No entries yet" in response.content


@pytest.mark.django_db
class TestGratitudeAddView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="gratadd", password="testpass123")

    def test_add_creates_entry(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.post("/journal/gratitude/add/", {"entry": "Good coffee"})
        assert response.status_code == 200  # HTMX partial response
        assert GratitudeEntry.objects.filter(user=user).count() == 1
        assert GratitudeEntry.objects.first().entry == "Good coffee"

    def test_add_increments_order(self, client: Client, user: User) -> None:
        today = timezone.now().date()
        GratitudeEntry.objects.create(user=user, date=today, entry="First", order=1)
        client.force_login(user)
        client.post("/journal/gratitude/add/", {"entry": "Second"})
        second = GratitudeEntry.objects.filter(user=user, entry="Second").first()
        assert second is not None
        assert second.order == 2

    def test_add_returns_updated_list(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.post("/journal/gratitude/add/", {"entry": "A warm bed"})
        assert b"A warm bed" in response.content


@pytest.mark.django_db
class TestGratitudeDeleteView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="gratdel", password="testpass123")

    def test_delete_removes_entry(self, client: Client, user: User) -> None:
        today = timezone.now().date()
        entry = GratitudeEntry.objects.create(user=user, date=today, entry="To delete")
        client.force_login(user)
        response = client.delete(f"/journal/gratitude/{entry.pk}/delete/")
        assert response.status_code == 200
        assert GratitudeEntry.objects.filter(pk=entry.pk).count() == 0

    def test_delete_other_user_entry_fails(self, client: Client, user: User) -> None:
        other = User.objects.create_user(username="other", password="testpass123")
        today = timezone.now().date()
        entry = GratitudeEntry.objects.create(user=other, date=today, entry="Not yours")
        client.force_login(user)
        client.delete(f"/journal/gratitude/{entry.pk}/delete/")
        # Entry should still exist (belongs to other user)
        assert GratitudeEntry.objects.filter(pk=entry.pk).count() == 1


@pytest.mark.django_db
class TestGratitudeHistoryView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="grathist", password="testpass123")

    def test_history_requires_login(self, client: Client) -> None:
        response = client.get("/journal/gratitude/history/")
        assert response.status_code == 302

    def test_history_shows_grouped_entries(self, client: Client, user: User) -> None:
        GratitudeEntry.objects.create(
            user=user, date=datetime.date(2024, 7, 4), entry="Independence", order=1
        )
        client.force_login(user)
        response = client.get("/journal/gratitude/history/")
        assert response.status_code == 200
        assert b"July 4, 2024" in response.content
        assert b"Independence" in response.content

    def test_history_empty_state(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/journal/gratitude/history/")
        assert b"No gratitude entries yet" in response.content


@pytest.mark.django_db
class TestDashboardGratitudeWidget:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="dashgrat", password="testpass123")

    def test_dashboard_no_gratitude(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/dashboard/")
        assert b"No entries yet today" in response.content

    def test_dashboard_with_gratitude(self, client: Client, user: User) -> None:
        today = timezone.now().date()
        GratitudeEntry.objects.create(user=user, date=today, entry="Test", order=1)
        GratitudeEntry.objects.create(user=user, date=today, entry="Test2", order=2)
        client.force_login(user)
        response = client.get("/dashboard/")
        content = response.content.decode()
        assert "2" in content  # count
        assert "entries today" in content
