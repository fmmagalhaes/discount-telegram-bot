import os
from bs4 import BeautifulSoup
from datetime import datetime
from common.discount import Discount
from scrappers.bs_selection_helper import get_selection_text
from scrappers.scrapper import Scrapper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

OPENBANK_DISCOUNTS_URL = "https://www.openbank.pt/descontos-bancarios"
DISCOUNT_CARD_CLASS = "MbDiscountCardstyled__AnimationWrapper-"


def load_browser():
    options = Options()
    options.headless = True
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"')
    if os.name == "nt":
        service = Service(ChromeDriverManager().install())
    else:
        service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)


class OpenBankScrapper(Scrapper):

    @property
    def source(self):
        return "OpenBank"

    def get_discounts(self):
        source = self.source

        print(f"{datetime.now().time()}: {source} - getting discounts")
        browser = load_browser()
        print(f"{datetime.now().time()}: {source} - loaded {browser.name} driver")

        # my raspberry sucks, we need a big timeout
        browser.set_page_load_timeout(30*60)
        browser.get(OPENBANK_DISCOUNTS_URL)
        print(f"{datetime.now().time()}: {source} - opened page")

        discounts = []
        WebDriverWait(browser, 5*60).until(EC.presence_of_element_located(
            (By.XPATH,  f'//div[contains(@class, "{DISCOUNT_CARD_CLASS}")]')))

        print(f"{datetime.now().time()}: {source} - loaded page")

        soup = BeautifulSoup(browser.page_source, "html.parser")

        # we could find the discounts with Selenium, but I like BeautifulSoup :)
        soup_discounts = soup.select(f'div[class*="{DISCOUNT_CARD_CLASS}"]')

        for soup_discount in soup_discounts:
            content = get_selection_text(soup_discount, 'div[class*="__ContentWrapper-"]', "\n")

            discount = Discount(content)
            discounts.append(discount)

        print(f"{datetime.now().time()}: {source} - got {len(discounts)} discounts\n")

        return discounts
