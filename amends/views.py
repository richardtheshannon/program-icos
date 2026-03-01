from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from amends.forms import AmendForm, PersonForm
from amends.models import Amend, Person


class PersonListView(ListView):
    """List all people on the user's amends list."""

    model = Person
    template_name = "amends/person_list.html"
    context_object_name = "people"

    def get_queryset(self):
        return Person.objects.filter(user=self.request.user)


class PersonCreateView(View):
    """Add a new person to the amends list."""

    def get(self, request: HttpRequest) -> HttpResponse:
        form = PersonForm()
        return render(request, "amends/person_form.html", {
            "form": form,
            "action": "Add",
        })

    def post(self, request: HttpRequest) -> HttpResponse:
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            messages.success(request, f"{person.name} added to your amends list.")
            return redirect("person_detail", pk=person.pk)
        return render(request, "amends/person_form.html", {
            "form": form,
            "action": "Add",
        })


class PersonUpdateView(View):
    """Edit a person on the amends list."""

    def get(self, request: HttpRequest, pk: str) -> HttpResponse:
        person = get_object_or_404(Person, pk=pk, user=request.user)
        form = PersonForm(instance=person)
        return render(request, "amends/person_form.html", {
            "form": form,
            "person": person,
            "action": "Edit",
        })

    def post(self, request: HttpRequest, pk: str) -> HttpResponse:
        person = get_object_or_404(Person, pk=pk, user=request.user)
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, f"{person.name} updated.")
            return redirect("person_detail", pk=person.pk)
        return render(request, "amends/person_form.html", {
            "form": form,
            "person": person,
            "action": "Edit",
        })


class PersonDeleteView(View):
    """Delete a person from the amends list (with confirmation)."""

    def get(self, request: HttpRequest, pk: str) -> HttpResponse:
        person = get_object_or_404(Person, pk=pk, user=request.user)
        return render(request, "amends/person_confirm_delete.html", {
            "person": person,
        })

    def post(self, request: HttpRequest, pk: str) -> HttpResponse:
        person = get_object_or_404(Person, pk=pk, user=request.user)
        name = person.name
        person.delete()
        messages.success(request, f"{name} removed from your amends list.")
        return redirect("person_list")


class PersonDetailView(View):
    """Full amend workflow for a person: Step 8 info + Step 9 amend tracking."""

    def get(self, request: HttpRequest, pk: str) -> HttpResponse:
        person = get_object_or_404(Person, pk=pk, user=request.user)
        amend = person.latest_amend()
        amend_form = AmendForm(instance=amend)
        return render(request, "amends/person_detail.html", {
            "person": person,
            "amend": amend,
            "amend_form": amend_form,
            "status_choices": Amend.Status.choices,
        })


class AmendCreateView(View):
    """Create or update the amend record for a person."""

    def post(self, request: HttpRequest, pk: str) -> HttpResponse:
        person = get_object_or_404(Person, pk=pk, user=request.user)
        amend = person.latest_amend()
        form = AmendForm(request.POST, instance=amend)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.person = person
            obj.save()
            messages.success(request, "Amend progress saved.")
            return redirect("person_detail", pk=person.pk)
        return render(request, "amends/person_detail.html", {
            "person": person,
            "amend": amend,
            "amend_form": form,
            "status_choices": Amend.Status.choices,
        })
