import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Tournament, Race, Participant, ParticipantCountry
from .utils import Website, generate_participants, RaceNotFound, export_csv, export_zip, get_files_list


def home(request):
    return render(request, "index.html")


@csrf_exempt
def scrap_race(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        body = json.loads(body)

        race_id = body.get("race_id")
        details = body.get("details")

        if race_id:

            try:
                race = Race.objects.get(fis_id=race_id)
            except Race.DoesNotExist:
                try:
                    website = Website(race_id, details)
                except RaceNotFound:
                    return HttpResponse(status=404)
                tournament, _ = Tournament.objects.get_or_create(name=website.get_race_tournament())

                race = Race.objects.create(
                    fis_id=race_id,
                    tournament=tournament,
                    place=website.get_race_place(),
                    date=website.get_date(),
                    kind=website.get_kind(),
                    hill_size=website.get_hill_size()
                )

                generate_participants(website, race)

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
