from django.test import TestCase, Client, tag, RequestFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.sessions.middleware import SessionMiddleware
from selenium import webdriver
from unittest import skip
from django.urls import reverse
from django.core.cache import cache
from django.core.management import call_command
from .models import Card, Band
from .views import *
import json
from urllib.parse import urlencode
from time import sleep

# code for creating fake requests with sessions for use in tests
request_factory = RequestFactory()


def fake_request(url=reverse("quiz_question"), data={}, with_session=True):
    r = request_factory.get(url, data)
    middleware = SessionMiddleware()
    middleware.process_request(r)
    r.session.save()
    return r


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
        get_params = {
            "name": obj['name'],
            "choice": choice,
        }
        # querystring = "?"+urlencode({
        #     "name": obj['name'],
        #     "choice": choice,
        # })

        response = self.client.get(reverse("quiz_question"), get_params)
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
        get_params = {
            "name": obj['name'],
            "choice": choice,
        }
        # querystring = "?" + urlencode({
        #     "name": obj['name'],
        #     "choice": choice,
        # })
        response = self.client.get(reverse("quiz_question"), get_params)
        obj = response.json()
        self.assertTrue(obj['streak'] == 0)
        self.assertTrue(obj['correctness'] == "incorrect")
        print(question_model.objects.first().incorrect)
        self.assertTrue(question_model.objects.first().incorrect == 1)
###################################################
    # testing the subroutines of the main view

    def test_handle_first_question(self):
        r = fake_request()
        result = handle_first_question(r)
        obj = json.loads(str(result.content, encoding="utf8"))
        self.assertTrue(r.session['streak'] == 0)
        self.assertTrue(r.session['current_question']['name'] in ['A Card', 'A Band'])
        self.assertTrue(obj['name'] == r.session['current_question']['name'])
        self.assertTrue(obj['streak'] == 0)
        self.assertTrue(obj['correctness'] == 'NA')
        self.assertTrue(obj['previous_name'] == 'NA')
        self.assertTrue(obj['previous_guess'] == 'NA')



###################################################
    # testing model methods

    def test_model_str(self):
        # str method of card/band models should just return the name of the object
        band = Band.objects.first()
        band_name = band.name
        self.assertTrue(band_name == str(band))

        card = Card.objects.first()
        card_name = card.name
        self.assertTrue(card_name == str(card))

###################################################
# new test class for selenium browser tests


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

    @tag("browser")
    def testRender(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
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

