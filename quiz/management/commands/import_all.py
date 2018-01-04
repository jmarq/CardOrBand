from django.core.management.base import BaseCommand
from quiz.utilities.cards.parse_cards import get_cards_by_color
from quiz.utilities.bands.get_bands import get_all_wiki_pages
from quiz.models import Card, Band

class Command(BaseCommand):
    def handle(self, *args, **options):

        # Card.objects.all().delete()
        # Band.objects.all().delete()

        cards = get_cards_by_color()
        bands = get_all_wiki_pages()

        self.stdout.write("*"*20)
        self.stdout.write("cards:\n")
        for card in cards:
            self.stdout.write(card)
            Card.objects.get_or_create(name=card)

        self.stdout.write("*" * 20)
        self.stdout.write("bands:\n")
        for band in bands:
            self.stdout.write(band)
            Band.objects.get_or_create(name=band)

        self.stdout.write("%d cards, %d bands" % (Card.objects.count(), Band.objects.count()))


