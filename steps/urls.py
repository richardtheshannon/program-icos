from django.urls import path

from steps.views import StepListView, step_detail_view

urlpatterns = [
    path("", StepListView.as_view(), name="step_list"),
    path("<int:step_number>/", step_detail_view, name="step_detail"),
]
