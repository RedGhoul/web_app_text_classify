from django.conf.urls import handler404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import record
import json
from .NLTKProcessor import extract_key_phrases_from_text, generate_summary, extract_summary_from_text, extract_sentiment
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, "nlp/index.html", context={})


def coming_soon(request):
    return render(request, "nlp/comeingsoon.html", context={})


def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        if user is not None:
            login(request, user)
            return redirect("nlp:index")
        else:
            return handler404(request)
    else:
        return render(request, "nlp/register.html", context={})

@csrf_exempt
def extract_key_phrases_from_text_view(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body['data'] is None:
            return json.dumps({"error" : "No Data Found"})

        final = extract_key_phrases_from_text(body['data'])

        nlprecord = record(api_name="extract_key_phrases_from_text", input_text=body['data'],
                           output_text=json.dumps({"rank_list": final}))

        nlprecord.save()

        return HttpResponse(str(json.dumps({"rank_list": final})))
    else:
        return HttpResponse("Nothing found")


@csrf_exempt
def extract_summary_from_text_view(request):
    if request.method == 'POST':

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body['data'] is None:
            return json.dumps({"error" : "No Data Found"})

        final = extract_summary_from_text(body['data']).replace("  ", " ")

        nlprecord = record(api_name="extract_summary_from_text", input_text=body['data'], output_text=final)

        nlprecord.save()

        return HttpResponse(str(json.dumps({"SummaryText": final})))
    else:
        return HttpResponse("Nothing found")

@csrf_exempt
def extract_sentiment_from_text_view(request):
    if request.method == 'POST':

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body['data'] is None:
            return json.dumps({"error" : "No Data Found"})

        final = extract_sentiment(body['data'])

        nlprecord = record(api_name="extract_sentiment_from_text",
                           input_text=body['data'], output_text=json.dumps(final))

        nlprecord.save()
        # always look at the compound score
        # {'pos': 0.746, 'compound': 0.8316, 'neu': 0.254, 'neg': 0.0}
        return HttpResponse(str(json.dumps(final)))
    else:
        return HttpResponse("Nothing found")