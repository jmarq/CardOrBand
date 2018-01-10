from django.test import TestCase, Client, tag
from unittest import skip
from django.urls import reverse
from django.core.cache import cache
from django.core.management import call_command
from .models import Card, Band
import json
from urllib.parse import urlencode



class ImportQuestionsTest(TestCase):
    def setUp(self):
        pass

    @tag("slow")
    def test_import_cards(self):
        call_command("import_cards")
        self.assertTrue(Card.objects.count() > 0)

    @tag("slow")
    def test_import_bands(self):
        call_command("import_bands")
        self.assertTrue(Band.objects.count() > 0)

    @tag("slow")
    def test_import_all(self):
        Card.objects.all().delete()
        Band.objects.all().delete()
        call_command("import_all")
        self.assertTrue(Card.objects.count() > 0)
        self.assertTrue(Band.objects.count() > 0)




class QuizTest(TestCase):
    def setUp(self):
        Card.objects.create(name="A Card")
        Band.objects.create(name="A Band")
        pass

    def test_quiz_home_view(self):
        response = self.client.get(reverse("quiz_home"))
        self.assertTrue(response.status_code == 200)

    def test_quiz_question_view(self):
        # get initial question
        response = self.client.get(reverse("quiz_question"))
        obj = response.json()
        self.assertTrue(obj['streak'] == 0)
        self.assertTrue(obj['correctness'] == "NA")
        self.assertTrue(obj['name'] in ["A Card", "A Band"])
        current_name = obj['name']
        # send another request without an appropriate answer
        response = self.client.get(reverse("quiz_question"))
        obj = response.json()
        self.assertTrue(obj['streak'] == 0)
        self.assertTrue(obj['correctness'] == "NA")
        # did it give us the same name as last time?
        self.assertTrue(obj['name'] == current_name)
        #prepare a correct answer
        if obj['name'] == "A Card":
            choice = "Card"
        else:
            choice = "Band"
        querystring = "?"+urlencode({
            "name": obj['name'],
            "choice": choice,
        })

        response = self.client.get(reverse("quiz_question")+querystring)
        obj = response.json()
        self.assertTrue(obj['streak'] == 1)
        self.assertTrue(obj['correctness'] == "correct")

        # now send a wrong answer for the new question
        if obj['name'] == "A Card":
            choice = "Band"
        else:
            choice = "Card"
        querystring = "?" + urlencode({
            "name": obj['name'],
            "choice": choice,
        })
        response = self.client.get(reverse("quiz_question") + querystring)
        obj = response.json()
        self.assertTrue(obj['streak'] == 0)
        self.assertTrue(obj['correctness'] == "incorrect")



    def test_model_str(self):
        # str method of card/band models should just return the name of the object
        band = Band.objects.first()
        band_name = band.name
        self.assertTrue(band_name == str(band))

        card = Card.objects.first()
        card_name = card.name
        self.assertTrue(card_name == str(card))
