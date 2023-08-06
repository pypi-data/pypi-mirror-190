import datetime
import requests
from dateutil.parser import parse
from bs4 import BeautifulSoup

GENERAL_WASTE = "General waste"
RECYCLING = "Recycling"
ORGANICS = "Green organics"
ADDRESS_LOOKUP_URL = "https://www.goldcoast.qld.gov.au/api/v1/myarea/search?keywords="
BIN_DAY_LOOKUP_URL = "https://www.goldcoast.qld.gov.au/ocapi/Public/myarea/wasteservices?ocsvclang=en-AU&geolocationid="
USER_AGENT_STRING = "gcbinspy api"

class AddressException(Exception):
    pass


class GoldCoastBins(object):
    def __init__(self, address=None, propertyid=None) -> None:
        self.propertyid = propertyid
        self.address = address
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT_STRING})
        if propertyid == None:
            self._get_property_id()

    # Try to find the property ID from address
    def _get_property_id(self) -> None:
        r = requests.get(f"{ADDRESS_LOOKUP_URL}{self.address}")
        if len(r.json()["Items"]) == 0:
            raise AddressException("No Property ID found for provided address.")
        id = r.json()["Items"][0]["Id"]
        print(f"Setting property ID to {id}")
        self.propertyid = id

    # Update next bin collection
    def update_next_bin_days(self):
        if self.propertyid == None:
            raise AddressException("No property ID has been set")
        r = requests.get(f"{BIN_DAY_LOOKUP_URL}{self.propertyid}")
        resp = r.json()["responseContent"]
        soup = BeautifulSoup(resp, "html.parser")
        arts = soup.find_all("article")
        for art in arts:
            o = {}
            t = art.h3.get_text("", strip=True)
            d = art.find("div", class_="next-service").get_text("", strip=True)
            o["type"] = t
            o["data"] = d
            if t == GENERAL_WASTE:
                self._set_landfill(d)
            if t == RECYCLING:
                self._set_recycling(d)
            if t == ORGANICS:
                self._set_organics(d)

    def _set_landfill(self, date) -> None:
        self.landfill = self._format_date(date)

    def _set_recycling(self, date) -> None:
        self.recycling = self._format_date(date)

    def _set_organics(self, date) -> None:
        self.organics = self._format_date(date)

    def _format_date(self, date) -> datetime.date:
        dt = parse(date, dayfirst=True)
        return dt.date()

    def next_landfill(self) -> datetime.date:
        return self.landfill

    def next_recycling(self) -> datetime.date:
        return self.recycling

    def next_organics(self) -> datetime.date:
        return self.organics

    def property_id(self) -> str:
        return self.propertyid

    def is_landfill_day(self) -> bool:
        return datetime.date.today() == self.landfill

    def is_recycling_day(self) -> bool:
        return datetime.date.today() == self.recycling

    def is_organics_day(self) -> bool:
        return datetime.date.today() == self.organics

    def is_landfill_day_tomorrow(self) -> bool:
        return datetime.date.today() + datetime.timedelta(days=1) == self.landfill

    def is_recycling_day_tomorrow(self) -> bool:
        return datetime.date.today() + datetime.timedelta(days=1) == self.recycling

    def is_organics_day_tomorrow(self) -> bool:
        return datetime.date.today() + datetime.timedelta(days=1) == self.organics
