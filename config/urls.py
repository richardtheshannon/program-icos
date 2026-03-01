from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("steps/", include("steps.urls")),
    path("journal/", include("journal.urls")),
    path("", include("core.urls")),
]
