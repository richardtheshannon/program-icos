from django.urls import path

from steps.views import StepListView, auto_save_response, step_detail_view

urlpatterns = [
    path("", StepListView.as_view(), name="step_list"),
    path("auto-save/", auto_save_response, name="auto_save_response"),
    path("<int:step_number>/", step_detail_view, name="step_detail"),
]
