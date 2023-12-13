
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from common.discount import Discount
from scrappers.bs_selection_helper import get_selection_text, get_selection_link
from scrappers.scrapper import Scrapper

MBWAY_DISCOUNTS_URL = "https://www.mbway.pt/promocoes/"
HEADERS_MBWAY = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9,pt-US;q=0.8,pt;q=0.7,en-US;q=0.6,nl;q=0.5",
    "Accept-Encoding": "gzip",
    "Referer": f"{MBWAY_DISCOUNTS_URL}/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "Cache-Control": "max-age=0",
}


class MBWayScrapper(Scrapper):

    @property
    def source(self):
        return "MBWay"

    def get_discounts(self):
        source = self.source

        print(f"{datetime.now().time()}: {self.source} - getting discounts")

        response = requests.get(MBWAY_DISCOUNTS_URL, headers=HEADERS_MBWAY)
        soup = BeautifulSoup(response.text, "html.parser")

        soup_discounts = soup.select("#desconto-container")

        discounts = []
        for soup_discount in soup_discounts:
            link = get_selection_link(soup_discount, "a")
            text = get_selection_text(soup_discount, ".teaser-desconto p", " ")

            discount = Discount(f"{link}\n{text}")
            discounts.append(discount)

        print(f"{datetime.now().time()}: {source} - got {len(discounts)} discounts\n")
        return discounts
