from __future__ import annotations

from django.http import HttpRequest


def active_section(request: HttpRequest) -> dict[str, str | None]:
    path = request.path or "/"
    if path.startswith("/dashboard"):
        section: str | None = "dashboard"
    elif path.startswith("/steps"):
        section = "steps"
    elif path.startswith("/journal"):
        section = "journal"
    elif path.startswith("/amends"):
        section = "amends"
    else:
        section = None
    return {"active_section": section}
