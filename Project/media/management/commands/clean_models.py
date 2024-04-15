
from django.core.management.base import BaseCommand, CommandError
from media.models import Media


class Command(BaseCommand):
    help = "Download IMDB Database"

    def handle(self, *args, **options):
        Media.objects.all().delete()