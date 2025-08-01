from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")

        if not User.objects.filter(username="user").exists():
            user1 = User.objects.create_user(username="user", email="user@example.com", password="userpass")

