from django.shortcuts import render
from django.http import JsonResponse
from quiz.utilities.random_choice import random_card_or_band
from .models import Card, Band
from django.db.models import F
import json


def quiz_question(request):

    current_question = request.session.get("current_question", "")
    previous_question = request.session.get("previous_question", "NA")
    previous_guess = request.session.get("previous_guess", "NA")
    streak = request.session.get("streak", 0)

    if not current_question:
        # this is the first question in this session
        request.session['streak'] = 0
        question = random_card_or_band()
        request.session['current_question'] = question
        print(request.session.get("current_question", ""))
        data = {
            "name": question["name"],
            "streak": 0,
            "correctness": "NA",
            "previous_name": "NA",
            "previous_guess": "NA",
        }
        return JsonResponse(data)
    else:
        # user has a question to answer.
        choice = request.GET.get("choice", "")
        question_name = request.GET.get("name", "")
        # are they sending an answer? to that question?
        if question_name != current_question['name'] or not choice:
            # user is answering the wrong question, or they didn't enter a choice
            print("no choice made, or choice made for wrong question")
            print("expected question for %s, got %s" % (current_question['name'], question_name))
            print("correct answer is %s" % current_question['type'])
            data = {
                "name": current_question["name"],
                "streak": request.session.get("streak"),
                "correctness": "NA" if choice or previous_question == "NA"
                else "correct" if previous_guess == previous_question['type']
                else "incorrect",
                "previous_name": "NA" if previous_question == "NA" else previous_question['name'],
                "previous_guess": previous_guess,
            }
            return JsonResponse(data)
        else:
            # user has entered an answer, user is answering the correct question
            # check for correctness
            if choice == current_question['type']:
                # correct!
                # get db object to increment its 'correct' counter
                if current_question['type'] == "Band":
                    obj = Band.objects.get(name=current_question['name'])
                else:
                    obj = Card.objects.get(name=current_question['name'])
                obj.correct += 1
                obj.save()
                # update streak, prepare new question
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
                # get db object to increment its 'incorrect' counter
                if current_question['type'] == "Band":
                    obj = Band.objects.get(name=current_question['name'])
                else:
                    obj = Card.objects.get(name=current_question['name'])
                obj.incorrect += 1
                obj.save()
                # update streak, prepare new question
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


def quiz_home(request):
    return render(request, "quiz/main.html", {})

if __name__ == '__main__':
    pass

