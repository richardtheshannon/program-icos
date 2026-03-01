import pytest
from django.test import Client

from amends.models import Amend, Person
from core.models import User


@pytest.mark.django_db
class TestPersonModel:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="amendsuser", password="testpass123")

    def test_create_person(self, user: User) -> None:
        person = Person.objects.create(
            user=user, name="John", relationship="Friend", how_harmed="Lied to him"
        )
        assert str(person) == "John (Friend)"
        assert person.current_status() == Amend.Status.NOT_STARTED

    def test_person_without_relationship(self, user: User) -> None:
        person = Person.objects.create(user=user, name="Jane", how_harmed="Borrowed money")
        assert str(person) == "Jane"

    def test_current_status_with_amend(self, user: User) -> None:
        person = Person.objects.create(user=user, name="Bob", how_harmed="Was dishonest")
        Amend.objects.create(person=person, status=Amend.Status.DISCUSSED)
        assert person.current_status() == Amend.Status.DISCUSSED


@pytest.mark.django_db
class TestAmendModel:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="amendmodel", password="testpass123")

    def test_create_amend(self, user: User) -> None:
        person = Person.objects.create(user=user, name="Test", how_harmed="Test harm")
        amend = Amend.objects.create(person=person, status=Amend.Status.LETTER_DRAFTED)
        assert "Letter Drafted" in str(amend)


@pytest.mark.django_db
class TestPersonListView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="listview", password="testpass123")

    def test_requires_login(self, client: Client) -> None:
        response = client.get("/amends/")
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_list_shows_people(self, client: Client, user: User) -> None:
        Person.objects.create(user=user, name="Alice", how_harmed="Gossiped")
        client.force_login(user)
        response = client.get("/amends/")
        assert response.status_code == 200
        assert b"Alice" in response.content

    def test_list_empty_state(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/amends/")
        assert b"Your amends list is empty" in response.content

    def test_list_scoped_to_user(self, client: Client, user: User) -> None:
        other = User.objects.create_user(username="other", password="testpass123")
        Person.objects.create(user=other, name="Secret", how_harmed="Not visible")
        client.force_login(user)
        response = client.get("/amends/")
        assert b"Secret" not in response.content


@pytest.mark.django_db
class TestPersonCreateView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="createview", password="testpass123")

    def test_create_form_renders(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.get("/amends/add/")
        assert response.status_code == 200
        assert b"Add Person" in response.content

    def test_create_person(self, client: Client, user: User) -> None:
        client.force_login(user)
        response = client.post("/amends/add/", {
            "name": "Dave",
            "relationship": "Brother",
            "how_harmed": "Stole from him",
            "willingness_level": "3",
        })
        assert response.status_code == 302
        assert Person.objects.filter(user=user, name="Dave").count() == 1


@pytest.mark.django_db
class TestPersonDetailView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="detailview", password="testpass123")

    @pytest.fixture
    def person(self, user: User) -> Person:
        return Person.objects.create(
            user=user, name="Eve", relationship="Ex", how_harmed="Was dishonest"
        )

    def test_detail_renders(self, client: Client, user: User, person: Person) -> None:
        client.force_login(user)
        response = client.get(f"/amends/{person.pk}/")
        assert response.status_code == 200
        assert b"Eve" in response.content
        assert b"Step 8" in response.content
        assert b"Step 9" in response.content

    def test_detail_shows_do_not_send_warning(self, client: Client, user: User, person: Person) -> None:
        client.force_login(user)
        response = client.get(f"/amends/{person.pk}/")
        assert b"DO NOT SEND" in response.content

    def test_other_user_cannot_access(self, client: Client, person: Person) -> None:
        other = User.objects.create_user(username="intruder", password="testpass123")
        client.force_login(other)
        response = client.get(f"/amends/{person.pk}/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestAmendCreateView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="amendcreate", password="testpass123")

    @pytest.fixture
    def person(self, user: User) -> Person:
        return Person.objects.create(user=user, name="Frank", how_harmed="Broke trust")

    def test_save_amend_progress(self, client: Client, user: User, person: Person) -> None:
        client.force_login(user)
        response = client.post(f"/amends/{person.pk}/amend/", {
            "status": "letter_drafted",
            "anger_letter": "I was so angry because...",
            "apology_letter": "",
            "actionable_amends": "",
            "sponsor_feedback": "",
            "post_amend_reflection": "",
        })
        assert response.status_code == 302
        amend = Amend.objects.get(person=person)
        assert amend.status == Amend.Status.LETTER_DRAFTED
        assert amend.anger_letter == "I was so angry because..."

    def test_update_existing_amend(self, client: Client, user: User, person: Person) -> None:
        Amend.objects.create(person=person, status=Amend.Status.NOT_STARTED)
        client.force_login(user)
        client.post(f"/amends/{person.pk}/amend/", {
            "status": "discussed",
            "anger_letter": "",
            "apology_letter": "",
            "actionable_amends": "",
            "sponsor_feedback": "Sponsor said go ahead",
            "post_amend_reflection": "",
        })
        assert Amend.objects.filter(person=person).count() == 1
        amend = Amend.objects.get(person=person)
        assert amend.status == Amend.Status.DISCUSSED
        assert amend.sponsor_feedback == "Sponsor said go ahead"


@pytest.mark.django_db
class TestPersonDeleteView:

    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(username="deleteview", password="testpass123")

    @pytest.fixture
    def person(self, user: User) -> Person:
        return Person.objects.create(user=user, name="Gone", how_harmed="Past")

    def test_delete_confirmation_renders(self, client: Client, user: User, person: Person) -> None:
        client.force_login(user)
        response = client.get(f"/amends/{person.pk}/delete/")
        assert response.status_code == 200
        assert b"Remove" in response.content
        assert b"Gone" in response.content

    def test_delete_removes_person(self, client: Client, user: User, person: Person) -> None:
        client.force_login(user)
        response = client.post(f"/amends/{person.pk}/delete/")
        assert response.status_code == 302
        assert Person.objects.filter(pk=person.pk).count() == 0
