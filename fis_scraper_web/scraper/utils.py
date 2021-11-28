import requests
from bs4 import BeautifulSoup

import fis_scraper_web.scraper.constants as const


class Website:

    def __init__(self, race_id: int):
        website = requests.get(f"{const.RACE_URL}{race_id}")
        self.soup = BeautifulSoup(website.content, features="html.parser")

    def get_race_place(self):
        return self.soup.select_one(const.PLACE_SELECTOR).text

    def get_race_tournament(self):
        return self.soup.select_one(const.TOURNAMENT_SELECTOR).text

    def has_details_view(self):
        return self.soup.select_one(const.DETAILS_SELECTOR).contents


if __name__ == '__main__':
    w = Website(6218)
    print(w.get_race_place())
    print(w.get_race_tournament())
    print(w.has_details_view())