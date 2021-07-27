from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "A description of the command"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('My sample command just ran.'))
