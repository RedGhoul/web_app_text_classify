from django.shortcuts import render
from django.http import HttpResponse
from .models import record
import json
from .NLTKProcessor import extract_key_phrases_from_text, generate_summary
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "nlp/index.html", context={})


def coming_soon(request):
    return render(request, "nlp/comeingsoon.html", context={})

@csrf_exempt
def extract_key_phrases_from_text(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body['data'] is None:
            return json.dumps({"rank_list": ""})

        final = extract_key_phrases_from_text(body['data'])

        nlprecord = record(api_name="extract_key_phrases_from_text", input_text=body['data'],
                           output_text=json.dumps({"rank_list": final}))

        nlprecord.save()

        return HttpResponse(str(json.dumps({"rank_list": final})))
    else:
        return HttpResponse("Nothing found")


@csrf_exempt
def extract_summary_from_text(request):
    if request.method == 'POST':

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body['data'] is None:
            return json.dumps({"rank_list": ""})

        final = generate_summary(body['data']).replace("  ", " ")

        nlprecord = record(api_name="extract_summary_from_text", input_text=body['data'], output_text=final)

        nlprecord.save()

        return HttpResponse(str(json.dumps({"SummaryText": final})))
    else:
        return HttpResponse("Nothing found")
