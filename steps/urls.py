from django.urls import path

from steps.views import (
    AllStepsExportView,
    StepExportView,
    StepListView,
    auto_save_response,
    step_detail_view,
)

urlpatterns = [
    path("", StepListView.as_view(), name="step_list"),
    path("auto-save/", auto_save_response, name="auto_save_response"),
    path("export/all/", AllStepsExportView.as_view(), name="export_all_steps"),
    path("<int:step_number>/", step_detail_view, name="step_detail"),
    path("<int:step_number>/export/", StepExportView.as_view(), name="export_step"),
]
