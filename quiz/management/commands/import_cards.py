from django.core.management.base import BaseCommand
from quiz.utilities.cards.parse_cards import get_cards_by_color
from quiz.models import Card

class Command(BaseCommand):
    def handle(self, *args, **options):
        cards = get_cards_by_color()
        for card in cards:
            self.stdout.write(card)
            Card.objects.get_or_create(name=card)


