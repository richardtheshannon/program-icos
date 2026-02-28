from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = "core/dashboard.html"


class PS01LoginView(LoginView):
    template_name = "core/login.html"
    redirect_authenticated_user = True


class PS01LogoutView(LogoutView):
    pass


def root_redirect(request: HttpRequest) -> HttpResponse:
    return redirect("dashboard")
