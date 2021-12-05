import json

from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Tournament, Race, Country, Jumper, ParticipantCountry, Jump, Participant
from .utils import Website
from . import maps


def home(request):
    return render(request, "index.html")


def generate_team_participants(website, race):
    rows = website.get_rows()
    for row in rows[0::5]:
        for line in row.select('div.g-row.justify-sb'):
            entries = list(map(website.get_text, line.select("div")))
            country_details = maps.map_team_country(entries)
            country, _ = Country.objects.update_or_create(name=country_details["name"],
                                                          defaults={"fis_code": country_details["fis_code"]})
            ParticipantCountry.objects.get_or_create(race=race,
                                                     country=country,
                                                     **maps.map_country_as_participant(
                                                         entries))

    for index, row in enumerate(rows):
        if index % 5 != 0:
            for line in row.select('div.g-row.justify-sb'):
                entries = list(map(website.get_text, line.select("div")))
                jumper, _ = Jumper.objects.get_or_create(**maps.map_team_jumper(entries))
                jump1_data, jump2_data = maps.map_team_jumps(entries)
                jump1, jump2 = None, None
                if jump1_data:
                    jump1 = Jump.objects.create(**jump1_data)
                if jump2_data:
                    jump2 = Jump.objects.create(**jump2_data)
                Participant.objects.get_or_create(race=race,
                                                  jumper=jumper,
                                                  jump_1=jump1,
                                                  jump_2=jump2)


def generate_detail_participants(website, race):
    rows = website.get_rows()
    for row in rows:
        country, jumper, jump_1, jump_2, participant, diff, other_params = None, None, None, None, None, None, None
        for index, line in enumerate(row.select('div.g-row.bb-xs')):
            entries = list(map(website.get_text, line.select("div")))
            if index == 0:
                country, _ = Country.objects.get_or_create(**maps.map_jumper_country_detail(entries))
                jumper, _ = Jumper.objects.update_or_create(**maps.map_details_jumper(entries),
                                                            defaults={"nation": country})
                other_params = maps.map_other_params_detail(entries)
            if index == 1:
                jump_1 = Jump.objects.create(**maps.map_detailed_jump(entries))
                diff = maps.map_diff_detail(entries).get("diff")
            if index == 2:
                jump_2 = Jump.objects.create(**maps.map_detailed_jump(entries))
            Participant.objects.get_or_create(jumper=jumper, jump_1=jump_1, jump_2=jump_2, diff=diff, race=race,
                                              **other_params)


def generate_simple_participants(website, race):
    rows = website.get_rows()
    for row in rows:
        for line in row.select('div.g-row.justify-sb'):
            jump_1, jump_2 = None, None
            entries = list(map(website.get_text, line.select("div")))
            print(entries)
            print(maps.map_simple_jump(entries))
            print(maps.map_simple_jumper(entries))
            print(maps.map_jumper_country_simple(entries))
            print(maps.map_other_params_simple(entries))
            country, _ = Country.objects.get_or_create(**maps.map_jumper_country_simple(entries))
            jumper, _ = Jumper.objects.update_or_create(**maps.map_simple_jumper(entries), defaults={"nation": country})
            jump_1_details, jump_2_details = maps.map_simple_jump(entries)
            if jump_1_details:
                jump_1 = Jump.objects.create(**jump_1_details)
            if jump_2_details:
                jump_2 = Jump.objects.create(**jump_2_details)
            Participant.objects.get_or_create(jumper=jumper, jump_1=jump_1, jump_2=jump_2, race=race,
                                              **maps.map_other_params_simple(entries))


def generate_participants(website, race):
    if website.is_team():
        generate_team_participants(website, race)
    elif website.has_details_view():
        generate_detail_participants(website, race)
    else:
        generate_simple_participants(website, race)


@csrf_exempt
def scrap_race(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        body = json.loads(body)

        race_id = body.get("race_id")
        details = body.get("details")

        website = Website(race_id, details)

        tournament, _ = Tournament.objects.get_or_create(name=website.get_race_tournament())
        race, _ = Race.objects.get_or_create(
            tournament=tournament,
            place=website.get_race_place(),
            date=website.get_date(),
            kind=website.get_kind(),
            hill_size=website.get_hill_size()
        )
        generate_participants(website, race)

    return JsonResponse(model_to_dict(race))
