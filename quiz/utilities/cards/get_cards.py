import requests

card_url = "https://mtgjson.com/json/AllCards.json"


def get_cards_json(url=card_url):
    r = requests.get(url)
    cards_json = r.json()
    return cards_json


# if __name__ == "__main__":
#     cards_json = get_cards_json()
#     print(cards_json.keys())
