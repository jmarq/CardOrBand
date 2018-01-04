import random
from quiz.models import Card, Band


def random_card_or_band():
    coin_flip = random.randint(0, 1)
    if coin_flip:
        model = Card
    else:
        model = Band
    instance = model.objects.all()[random.randint(0,model.objects.count()-1)]
    return {
        "name": instance.name,
        "type": model.__name__
    }


