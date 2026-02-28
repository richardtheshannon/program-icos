from django.urls import path

from core.views import DashboardView, PS01LoginView, PS01LogoutView, root_redirect

urlpatterns = [
    path("", root_redirect, name="root"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("login/", PS01LoginView.as_view(), name="login"),
    path("logout/", PS01LogoutView.as_view(), name="logout"),
]
