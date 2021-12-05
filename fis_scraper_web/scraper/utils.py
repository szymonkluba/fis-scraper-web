import datetime
import re

import requests
from bs4 import BeautifulSoup, Tag

from . import constants as const
from .sele import get_dynamic_content


class Website:

    def __init__(self, race_id: int, details: bool = False):
        self.race_id = race_id
        website = requests.get(f"{const.RACE_URL}{self.race_id}").content
        self.soup = BeautifulSoup(website, features="lxml")
        self.details = details and self.has_details_view()
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
        if tag.select_one(".country__name-short"):
            country = tag.select_one(".country__name-short").string
            return country.strip() if country else None
        return tag.string.strip() if tag.string else None


if __name__ == '__main__':
    w = Website(6221)
    rows: Tag = w.get_rows()
    for row in rows:
        # simple and team
        for line in row.select('div.g-row.justify-sb'):
            print(line.get_attribute_list("class"))
            for entry in line.select('div'):
                print(Website.get_text(entry))
        # details
        for line in row.select('div.g-row.bb-xs'):
            print(line.get_attribute_list("class"))
            for entry in line.select('div'):
                print(Website.get_text(entry))
