"""Django command to wait for the db to be available"""

from django.core.management.base import BaseCommand  # type: ignore


class Command(BaseCommand):
    """Django command to wait for the db"""

    def handle(self, *args, **options):
        pass
