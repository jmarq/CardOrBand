from django.core.management.base import BaseCommand
from quiz.utilities.bands.get_bands import get_all_wiki_pages
from quiz.models import Band

class Command(BaseCommand):
    def handle(self, *args, **options):
        bands = get_all_wiki_pages()
        for band in bands:
            self.stdout.write(band)
            Band.objects.get_or_create(name=band)


