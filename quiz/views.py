from django.shortcuts import render
from django.http import JsonResponse
from quiz.utilities.random_choice import random_card_or_band
from .models import Card, Band
from django.db.models import F
import json

# Create your views here.

def quiz_question(request):

    current_question = request.session.get("current_question", "")
    previous_question = request.session.get("previous_question", "NA")
    previous_guess = request.session.get("previous_guess", "NA")
    streak = request.session.get("streak",0)

    if not current_question:
    # this is the first question
        request.session['streak'] = 0
        question = random_card_or_band()
        request.session['current_question'] = question
        print(request.session.get("current_question", ""))
        data = {
            "name": question["name"],
            "streak": 0,
            "correctness": "NA",
            "previous_name": "NA",
            "previous_guess" : "NA",
        }
        return JsonResponse(data)
    else:
    # user has a question to answer. are they sending an answer? to that question? correct?
        choice = request.GET.get("choice","")
        question_name = request.GET.get("name","")
        if question_name != current_question['name'] or not choice:
            print("no choice made, or choice made for wrong question")
            print("expected question for %s, got %s" % (current_question['name'],question_name))
            print("correct answer is %s" % current_question['type'])
            # user is answering the wrong question, or they didn't enter a choice
            data = {
                "name": current_question["name"],
                "streak": request.session.get("streak"),
                "correctness": "NA" if choice else "correct" if previous_guess == previous_question['type'] else "incorrect",
                "previous_name": previous_question['name'],
                "previous_guess": previous_guess,
            }
            return JsonResponse(data)
        else:
            # user has entered an answer, user is answering the correct question
            # check for correctness
            if choice == current_question['type']:
                # correct!
                obj = ""
                if current_question['type'] == "Band":
                    obj = Band.objects.get(name=current_question['name'])
                else:
                    obj = Card.objects.get(name=current_question['name'])
                obj.correct = obj.correct + 1
                obj.save()

                request.session['streak'] = streak + 1
                question = random_card_or_band()
                request.session['previous_question'] = current_question
                request.session['previous_guess'] = choice
                request.session['current_question'] = question
                data = {
                    "name": question["name"],
                    "streak": streak + 1,
                    "correctness": "correct",
                    "previous_name": current_question['name'],
                    "previous_guess": choice,
                }
                return JsonResponse(data)
            else:
                # incorrect
                obj = ""
                if current_question['type'] == "Band":
                    obj = Band.objects.get(name=current_question['name'])
                else:
                    obj = Card.objects.get(name=current_question['name'])
                obj.incorrect = obj.correct + 1
                obj.save()
                request.session['streak'] = 0
                request.session['previous_question'] = current_question
                request.session['previous_guess'] = choice
                question = random_card_or_band()
                request.session['current_question'] = question

                data = {
                    "name": question["name"],
                    "streak": 0,
                    "correctness": "incorrect",
                    "previous_name": current_question['name'],
                    "previous_guess": choice,
                }
                return JsonResponse(data)

        pass

def quiz_home(request):
    return render(request, "quiz/main.html",{})

#def random_choice(request):
#     if request.session.get("waiting_for_answer",""):
#         # how to handle this? break the streak? just ignore the request, send back a warning?h
#         print("hmmm they asked for a choice but we were expecting an answer")
#         print("the right answer would have been %s" % request.session.get("right_answer", "???"))
#
#     choice = random_card_or_band()
#     data = {
#         "name": choice["name"],
#     }
#     request.session['waiting_for_answer'] = True
#     request.session['right_answer'] = choice['type']
#     return JsonResponse(data)
#
#
# def make_choice(request):
#     choice = request.GET.get("choice","")
#     data = {
#         "correct": False,
#         "message": "wasn't expecting an answer"
#     }
#     if choice:
#         if request.session.get("waiting_for_answer",""):
#             if choice == request.session.get("right_answer",""):
#                 streak = request.session.get("streak", 0)
#                 streak += 1
#                 request.session['streak'] = streak
#                 data = {
#                     "correct": True,
#                     "streak": streak,
#                 }
#             else:
#                 streak = 0
#                 request.session['streak'] = streak
#                 data = {
#                     "correct": False,
#                     "streak": streak,
#                 }
#             request.session['waiting_for_answer'] = False
#     return JsonResponse(data)

if __name__ == '__main__':
    pass

