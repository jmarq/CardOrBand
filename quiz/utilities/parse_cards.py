from get_cards import get_cards_json

cards_dict = get_cards_json()

keys = cards_dict.keys()

mono_black_cards = []

for key in keys:
    card = cards_dict[key]
    # card has colors, card colors is a list only containing Black
    if "colors" in card and card['colors']==["Black"]:
        mono_black_cards.append(key)

print(mono_black_cards)
print(len(mono_black_cards))
