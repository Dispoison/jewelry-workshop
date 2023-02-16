from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("-u", "--username", default="admin", type=str, help="Admin username, default `admin`")
        parser.add_argument("-p", "--password", default="admin", type=str, help="Admin password, default `admin`")
        parser.add_argument("-e", "--email", default="admin@example.com", type=str,
                            help="Admin email, default `admin@example.com`")

    def handle(self, **options):
        User.objects.create_superuser(options["username"], options["email"], options["password"])
