from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.static import serve

urlpatterns = [
    path(
        "manifest.webmanifest",
        TemplateView.as_view(
            template_name="manifest.webmanifest",
            content_type="application/manifest+json",
        ),
    ),
    path(
        "service-worker.js",
        serve,
        {
            "document_root": settings.BASE_DIR / "static",
            "path": "service-worker.js",
        },
    ),
    path("admin/", admin.site.urls),
    path("steps/", include("steps.urls")),
    path("journal/", include("journal.urls")),
    path("amends/", include("amends.urls")),
    path("", include("core.urls")),
]
