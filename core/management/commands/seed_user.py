from django.core.management.base import BaseCommand
from decouple import config

from core.models import User


class Command(BaseCommand):
    help = "Create seeded superuser from environment variables"

    def handle(self, *args: object, **options: object) -> None:
        email = config("PS01_USER_EMAIL")
        password = config("PS01_USER_PASSWORD")
        first_name = config("PS01_USER_FIRST_NAME", default="")
        last_name = config("PS01_USER_LAST_NAME", default="")

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"User {email} already exists — skipping."))
            return

        user = User.objects.create_superuser(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser created: {user.email}"))
