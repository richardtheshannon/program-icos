from django.urls import path

from amends.views import (
    AmendCreateView,
    PersonCreateView,
    PersonDeleteView,
    PersonDetailView,
    PersonListView,
    PersonUpdateView,
)

urlpatterns = [
    path("", PersonListView.as_view(), name="person_list"),
    path("add/", PersonCreateView.as_view(), name="person_create"),
    path("<uuid:pk>/", PersonDetailView.as_view(), name="person_detail"),
    path("<uuid:pk>/edit/", PersonUpdateView.as_view(), name="person_update"),
    path("<uuid:pk>/delete/", PersonDeleteView.as_view(), name="person_delete"),
    path("<uuid:pk>/amend/", AmendCreateView.as_view(), name="amend_create"),
]
