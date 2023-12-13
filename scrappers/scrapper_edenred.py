import random
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
from common.discount import Discount
from scrappers.bs_selection_helper import get_selection_text
from scrappers.scrapper import Scrapper

EDENRED_BASE_URL = "https://edenred.pt"
EDENRED_DISCOUNTS_URL = f"{EDENRED_BASE_URL}/programa-descontos-vantagens/"

# just in case, to avoid infinite loop in case something changes in the page
MAX_PAGE_NUMBER = 20

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9,pt-US;q=0.8,pt;q=0.7,en-US;q=0.6,nl;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": f"{EDENRED_BASE_URL}/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "Cache-Control": "max-age=0",
}


class EdenredScrapper(Scrapper):

    @property
    def source(self):
        return "Edenred"

    def get_discounts(self):
        source = self.source

        page_number = 1
        discounts = []

        while page_number <= MAX_PAGE_NUMBER:
            print(f"{datetime.now().time()}: {source} - getting discounts - page {page_number}")
            response = requests.get(f"{EDENRED_DISCOUNTS_URL}/page/{page_number}", headers=HEADERS)
            soup = BeautifulSoup(response.text, "html.parser")

            soup_discounts = soup.select(".benefits-container .benefits-col")

            if not soup_discounts:
                break

            for soup_discount in soup_discounts:
                header = get_selection_text(
                    soup_discount, ".benefits-header", " ")
                # they have a typo in the class name
                body_typo = get_selection_text(soup_discount, ".beneficts-body", " ")
                body = get_selection_text(soup_discount, ".benefits-body", " ")

                text = f"{header}\n{body if body else body_typo}"
                discount = Discount(text)
                discounts.append(discount)

            time.sleep(random.uniform(5, 10))
            page_number += 1

        print(f"{datetime.now().time()}: {source} - got {len(discounts)} discounts\n")
        return discounts
