from django.shortcuts import render
from django.http import JsonResponse
from quiz.utilities.random_choice import random_card_or_band

# Create your views here.

def random_choice(request):
    if request.session.get("waiting_for_answer",""):
        # how to handle this? break the streak? just ignore the request, send back a warning?h
        print("hmmm they asked for a choice but we were expecting an answer")
        print("the right answer would have been %s" % request.session.get("right_answer", "???"))

    choice = random_card_or_band()
    data = {
        "name": choice["name"],
    }
    request.session['waiting_for_answer'] = True
    request.session['right_answer'] = choice['type']
    return JsonResponse(data)


def make_choice(request):
    choice = request.GET.get("choice","")
    data = {
        "correct": False,
        "message": "wasn't expecting an answer"
    }
    if choice:
        if request.session.get("waiting_for_answer",""):
            if choice == request.session.get("right_answer",""):
                streak = request.session.get("streak", 0)
                streak += 1
                request.session['streak'] = streak
                data = {
                    "correct": True,
                    "streak": streak,
                }
            else:
                streak = 0
                request.session['streak'] = streak
                data = {
                    "correct": False,
                    "streak": streak,
                }
            request.session['waiting_for_answer'] = False
    return JsonResponse(data)
