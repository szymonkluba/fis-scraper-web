import csv
import datetime
import io
import re
import zipfile
from wsgiref.util import FileWrapper

import requests
from bs4 import BeautifulSoup, Tag
from django.http import HttpResponse, StreamingHttpResponse

from . import constants as const, maps
from .models import Country, Jumper, Jump, Participant, ParticipantCountry
from .sele import get_dynamic_content


class RaceNotFound(Exception):
    pass


class Website:

    def __init__(self, race_id: int, details: bool = False):
        self.race_id = race_id
        website = requests.get(f"{const.RACE_URL}{self.race_id}")
        if not website.ok:
            raise RaceNotFound
        self.soup = BeautifulSoup(website.content, features="lxml")
        self.details = False  # details and self.has_details_view()
        if self.details:
            website = get_dynamic_content(f"{const.RACE_URL}{self.race_id}{const.DETAILS_PARAM}")
        else:
            website = requests.get(f"{const.RACE_URL}{self.race_id}").content
        self.soup = BeautifulSoup(website, features="lxml")

    def get_race_place(self):
        return self.soup.select_one(const.PLACE_SELECTOR).text

    def get_race_tournament(self):
        return self.soup.select_one(const.TOURNAMENT_SELECTOR).text

    def has_details_view(self):
        return bool(self.soup.select_one(const.DETAILS_SELECTOR))

    def is_team(self):
        return self.get_kind() == "team"

    def get_date(self):
        return datetime.datetime.strptime(self.soup.select_one(const.DATE_SELECTOR).text, const.DATE_FORMAT)

    def get_hill_size(self):
        hill_size = re.findall(r"HS\d+", self.soup.select_one(const.KIND_SELECTOR).text)
        if hill_size:
            return hill_size[0]
        hill_size = re.findall(r"K\d+", self.soup.select_one(const.KIND_SELECTOR).text)
        if hill_size:
            return hill_size[0]
        hill_size = re.findall(r"\w+\sHill", self.soup.select_one(const.KIND_SELECTOR).text)
        if hill_size:
            return hill_size[0]

    def get_kind(self):
        kind = self.soup.select_one(const.KIND_SELECTOR).text
        kind = kind.replace(self.get_hill_size(), "").strip()
        if "Team" in kind:
            return "team"
        if "Women" in kind:
            return "women"
        if "Men" in kind:
            return "men"
        return "other"

    def get_rows(self):
        if self.details:
            return self.soup.select(const.ROW_DETAILED_SELECTOR)[3:]
        return self.soup.select(const.ROW_SIMPLE_SELECTOR)[1:]

    @staticmethod
    def get_text(tag: Tag):
        if tag.select_one(const.COUNTRY_SELECTOR):
            country = tag.select_one(const.COUNTRY_SELECTOR).string
            return country.strip() if country else None
        return tag.string.strip() if tag.string else None


def generate_team_participants(website, race):
    rows = website.get_rows()
    for row in rows[0::5]:
        for line in row.select(const.ENTRIES_SIMPLE_SELECTOR):
            entries = list(map(website.get_text, line.select(const.ENTRIES_INDIVIDUAL_SELECTOR)))
            country_details = maps.map_team_country(entries)
            country, _ = Country.objects.update_or_create(name=country_details["name"],
                                                          defaults={"fis_code": country_details["fis_code"]})
            ParticipantCountry.objects.get_or_create(race=race,
                                                     country=country,
                                                     **maps.map_country_as_participant(
                                                         entries))

    for index, row in enumerate(rows):
        if index % 5 != 0:
            for line in row.select(const.ENTRIES_SIMPLE_SELECTOR):
                entries = list(map(website.get_text, line.select(const.ENTRIES_INDIVIDUAL_SELECTOR)))
                jumper, _ = Jumper.objects.get_or_create(**maps.map_team_jumper(entries))
                jump1_data, jump2_data = maps.map_team_jumps(entries)
                jump1, jump2 = None, None
                if jump1_data:
                    jump1, _ = Jump.objects.get_or_create(**jump1_data)
                if jump2_data:
                    jump2, _ = Jump.objects.get_or_create(**jump2_data)
                Participant.objects.get_or_create(race=race,
                                                  jumper=jumper,
                                                  jump_1=jump1,
                                                  jump_2=jump2)


def generate_detail_participants(website, race):
    rows = website.get_rows()
    for row in rows:
        country, jumper, jump_1, jump_2, participant, diff, other_params = None, None, None, None, None, None, None
        for index, line in enumerate(row.select(const.ENTRIES_DETAILS_SELECTOR)):
            entries = list(map(website.get_text, line.select(const.ENTRIES_INDIVIDUAL_SELECTOR)))
            if index == 0:
                country, _ = Country.objects.get_or_create(**maps.map_jumper_country_detail(entries))
                jumper, _ = Jumper.objects.update_or_create(**maps.map_details_jumper(entries),
                                                            defaults={"nation": country})
                other_params = maps.map_other_params_detail(entries)
            if index == 1:
                jump_1, _ = Jump.objects.get_or_create(**maps.map_detailed_jump(entries))
                diff = maps.map_diff_detail(entries).get("diff")
            if index == 2:
                jump_2, _ = Jump.objects.get_or_create(**maps.map_detailed_jump(entries))
            participant, _ = Participant.objects.update_or_create(jumper=jumper, race=race,
                                                                  defaults={"jump_1": jump_1, "jump_2": jump_2,
                                                                            "diff": diff, **other_params})


def generate_simple_participants(website, race):
    rows = website.get_rows()
    for row in rows:
        for line in row.select(const.ENTRIES_SIMPLE_SELECTOR):
            jump_1, jump_2 = None, None
            entries = list(map(website.get_text, line.select(const.ENTRIES_INDIVIDUAL_SELECTOR)))
            country, _ = Country.objects.get_or_create(**maps.map_jumper_country_simple(entries))
            jumper_details = maps.map_simple_jumper(entries)
            jumper, _ = Jumper.objects.update_or_create(name=jumper_details["name"],
                                                        defaults={"nation": country, **jumper_details})
            jump_1_details, jump_2_details = maps.map_simple_jump(entries)
            if jump_1_details:
                jump_1, _ = Jump.objects.get_or_create(**jump_1_details)
            if jump_2_details:
                jump_2, _ = Jump.objects.get_or_create(**jump_2_details)
            Participant.objects.get_or_create(jumper=jumper, jump_1=jump_1, jump_2=jump_2, race=race,
                                              **maps.map_other_params_simple(entries))


def generate_participants(website, race):
    if website.is_team():
        generate_team_participants(website, race)
    elif website.has_details_view():
        generate_detail_participants(website, race)
    else:
        generate_simple_participants(website, race)


def export_csv(queryset, output):
    model = queryset.model
    model_fields = model._meta.fields + model._meta.many_to_many
    field_names = [f.name for f in model_fields]
    headers = []
    for field_name in [f.name for f in model_fields]:
        if field_name == "jump_1" or field_name == "jump_2":
            headers.extend([f.name for f in Jump._meta.fields])
        else:
            headers.append(field_name)
    print(headers)
    writer = csv.writer(output, dialect="excel")
    writer.writerow(headers)
    for row in queryset:
        values = []
        for field in field_names:
            value = getattr(row, field, None)
            if type(value) == Jump:
                for field_name in [field.name for field in Jump._meta.fields if field.name != "id"]:
                    if field_name != "id":
                        values.append(getattr(value, field_name))
            if value is None:
                value = ''
            if (field == "jump_1" and value == "") or (field == "jump_2" and value == ""):
                values.extend(["" for field in Jump._meta.fields if field.name != "id"])
            values.append(value)
        writer.writerow(values)
    return output


def export_zip(files, filename):
    temp_file = io.BytesIO()
    with zipfile.ZipFile(
        temp_file, "w", zipfile.ZIP_DEFLATED
    ) as opened_zip:
        for file in files:
            file["data"].seek(0)
            opened_zip.writestr(
                f"{file['filename']}.csv",
                file["data"].getvalue()
            )

    temp_file.seek(0)
    response = StreamingHttpResponse(
        FileWrapper(temp_file),
        content_type="application/zip",
    )

    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def get_files_list(queryset_list, filenames):

    files_list = []

    for index, queryset in enumerate(queryset_list):
        temp_file = io.StringIO()
        file = {
            "filename": filenames[index],
            "data": export_csv(queryset, temp_file)
        }
        files_list.append(file)

    return files_list