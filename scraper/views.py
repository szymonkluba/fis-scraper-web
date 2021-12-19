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


@csrf_exempt
def download_all(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        body = json.loads(body)
        race_ids = body.get("race_ids")
        if race_ids:
            queryset_list = []
            filenames = []
            for race_id in race_ids:
                race = Race.objects.get(fis_id=race_id)
                filename = str(race).replace(" ", "_")
                filenames.append(filename)
                queryset = Participant.objects.filter(race=race)
                queryset_list.append(queryset)

            return export_zip(get_files_list(queryset_list, filenames), f"{race_ids[0]}-{race_ids[-1]}")
        return HttpResponse(status=400)
    return HttpResponse(status=405)


@csrf_exempt
def archive(request):
    races = Race.objects.all()
    data = serializers.serialize("json", races)
    return JsonResponse(data, safe=False)
