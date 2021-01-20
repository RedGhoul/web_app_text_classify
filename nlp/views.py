from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import apistat, record
import json
from .NLTKProcessor import extract_key_phrases_from_text, generate_summary
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request,"nlp/index.html", context={})


def create_api_stat(name):
    cur_api_stat = apistat.objects.filter(name=name).first()
    if cur_api_stat is not None:
        cur_api_stat.hit_count = cur_api_stat.hit_count + 1
        cur_api_stat.save()
    else:
        new_apistat = apistat(name=name, hit_count=1)
        new_apistat.save()

@csrf_exempt
def extract_keyphrases_from_text(request):
    if request.method == 'POST':
        create_api_stat("extract_keyphrases_from_text")

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body['data'] is None:
            return json.dumps({"rank_list": ""})

        final = extract_key_phrases_from_text(body['data'])

        nlprecord = record(input_text=body['data'], output_text=json.dumps({"rank_list": final}))

        nlprecord.save()

        return HttpResponse(str(json.dumps({"rank_list": final})))
    else:
        return HttpResponse("Nothing found")

@csrf_exempt
def extract_summary_from_text(request):
    if request.method == 'POST':
        create_api_stat("extract_summary_from_text")

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body['data'] is None:
            return json.dumps({"rank_list": ""})

        final = generate_summary(body['data']).replace("  "," ")

        nlprecord = record(input_text=body['data'], output_text=final)

        nlprecord.save()

        return HttpResponse(str(json.dumps({"SummaryText":final})))
    else:
        return HttpResponse("Nothing found")


