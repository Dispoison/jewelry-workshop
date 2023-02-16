from django.core.management.base import BaseCommand

from workshop.database.db_init_data import db_init


class Command(BaseCommand):
    def handle(self, **options):
        db_init()
