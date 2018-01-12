from django.test import TestCase, Client, tag
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from unittest import skip
from django.urls import reverse
from django.core.cache import cache
from django.core.management import call_command
from .models import Card, Band
import json
from urllib.parse import urlencode
from time import sleep



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
            question_model = Card
        else:
            choice = "Band"
            question_model = Band
        querystring = "?"+urlencode({
            "name": obj['name'],
            "choice": choice,
        })

        response = self.client.get(reverse("quiz_question")+querystring)
        obj = response.json()
        self.assertTrue(obj['streak'] == 1)
        self.assertTrue(obj['correctness'] == "correct")
        self.assertTrue(question_model.objects.first().correct == 1)


        # now send a wrong answer for the new question
        if obj['name'] == "A Card":
            choice = "Band"
            question_model = Card

        else:
            choice = "Card"
            question_model = Band
        querystring = "?" + urlencode({
            "name": obj['name'],
            "choice": choice,
        })
        response = self.client.get(reverse("quiz_question") + querystring)
        obj = response.json()
        self.assertTrue(obj['streak'] == 0)
        self.assertTrue(obj['correctness'] == "incorrect")
        print(question_model.objects.first().incorrect)
        self.assertTrue(question_model.objects.first().incorrect == 1)



    def test_model_str(self):
        # str method of card/band models should just return the name of the object
        band = Band.objects.first()
        band_name = band.name
        self.assertTrue(band_name == str(band))

        card = Card.objects.first()
        card_name = card.name
        self.assertTrue(card_name == str(card))


class SeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        super(SeleniumTests, self).setUp()
        self.selenium = webdriver.Chrome()
        self.selenium.implicitly_wait(2)
        Card.objects.create(name="A Card")
        Band.objects.create(name="A Band")

    def tearDown(self):
        self.selenium.quit()
        super(SeleniumTests, self).tearDown()

    def testRender(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/quiz/'))
        body = self.selenium.find_element_by_tag_name("body")
        question_element = self.selenium.find_element_by_class_name("question")
        question_text = question_element.text
        if "Card" in question_text:
            button_class = "card-button"
        else:
            button_class = "band-button"
        correct_button = self.selenium.find_element_by_class_name(button_class)
        correct_button.click()
        initial_feedback = self.selenium.find_element_by_class_name("initial-feedback")
        self.assertTrue("correct" in initial_feedback.text)
        body_class = body.get_attribute("class")
        self.assertTrue(body_class == "correct")
        next_button = self.selenium.find_element_by_class_name("next")
        next_button.click()
        body_class = body.get_attribute("class")
        self.assertTrue(body_class == "")

