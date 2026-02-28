from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """Redirect unauthenticated users to login page.

    Exempt paths: /login/, /admin/, /static/
    """

    EXEMPT_PREFIXES = ("/login/", "/admin/", "/static/")

    def __init__(self, get_response: callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_authenticated:
            if not any(request.path.startswith(p) for p in self.EXEMPT_PREFIXES):
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)
