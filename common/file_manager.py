import json
import os
import sys
import yaml
from datetime import datetime
from common.discount import DiscountGroup

DISCOUNTS_FILE = "discounts.json"


def load_bot_config():
    with open(os.path.join(sys.path[0], "bot.yaml"), "r") as f:
        return yaml.safe_load(f)


def load_discounts_from_file() -> list[DiscountGroup]:
    try:
        with open(os.path.join(sys.path[0], DISCOUNTS_FILE), "r", encoding="utf-8") as file:
            json_discounts = json.load(file)
            discounts = []
            for discount in json_discounts:
                discounts.append(DiscountGroup.fromJson(discount))
            return discounts
    except FileNotFoundError:
        return []


# https://stackoverflow.com/a/64469761/8840143
def save_discounts_to_file(discount_groups: list[DiscountGroup]):
    discounts_json = json.dumps(discount_groups, indent=4, default=vars, ensure_ascii=False)

    with open(os.path.join(sys.path[0], DISCOUNTS_FILE), "w", encoding="utf8") as file:
        file.write(discounts_json)

    print(f"{datetime.now().time()}: discounts were saved in file")
