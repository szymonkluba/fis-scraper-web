import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Race, Participant, ParticipantCountry
from .utils import export_csv, export_zip, get_files_list, get_race


def home(request):
    return render(request, "index.html")


@csrf_exempt
def scrap_race(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        body = json.loads(body)
        race_id = body.get("race_id")
        details = body.get("details", False)
        if race_id:
            race = get_race(race_id, details)
            data = serializers.serialize("json", [race])
            return JsonResponse(data, safe=False)
        return HttpResponse(status=400)
    return HttpResponse(status=405)


@csrf_exempt
def scrap_races_list(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        body = json.loads(body)
        race_ids = body.get("race_ids")
        details = body.get("details", False)
        if race_ids:
            races = []
            for race_id in race_ids:
                race = get_race(race_id, details)
                races.append(race)
            data = serializers.serialize("json", races)
            return JsonResponse(data, safe=False)
        return HttpResponse(status=400)
    return HttpResponse(status=405)


@csrf_exempt
def scrap_races_range(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        body = json.loads(body)
        start = int(body.get("start"))
        end = int(body.get("end")) + 1
        details = body.get("details", False)
        if start and end:
            races = []
            for race_id in range(start, end):
                race = get_race(race_id, details)
                races.append(race)
            data = serializers.serialize("json", races)
            return JsonResponse(data, safe=False)
        return HttpResponse(status=400)
    return HttpResponse(status=500)


@csrf_exempt
def download_csv(request, race_id):
    if race_id:
        race = Race.objects.get(pk=race_id)
        participants = Participant.objects.prefetch_related("jump_1", "jump_2").filter(race=race)
        filename = str(race).replace(" ", "_")
        if race.kind != "team":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

            return export_csv(participants, response)

        participants_countries = ParticipantCountry.objects.filter(race=race)
        filenames = [
            filename + "_countries",
            filename + "_jumpers",
        ]
        queryset_list = [
            participants_countries,
            participants,
        ]

        return export_zip(get_files_list(queryset_list, filenames), filename)
