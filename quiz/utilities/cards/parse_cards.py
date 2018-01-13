from .get_cards import get_cards_json


def get_cards_by_color(color="Black"):
    cards_dict = get_cards_json()
    keys = cards_dict.keys()
    selected_cards = []

    for key in keys:
        card = cards_dict[key]
        # card has colors, card colors is a list only containing Black
        if "colors" in card and card['colors'] == [color]:
            selected_cards.append(key)

    return selected_cards

# if __name__ == "__main__":
#     cards = get_cards_by_color("Green")
#     print(cards)
#     print(len(cards))
