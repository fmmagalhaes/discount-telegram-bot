import random
import traceback
from datetime import datetime
from common.discount import DiscountGroup
from common.error_handler import handle_error
from common.file_manager import load_discounts_from_file, save_discounts_to_file, load_bot_config
from scrappers.scrapper_mbway import MBWayScrapper
from scrappers.scrapper_openbank import OpenBankScrapper
from scrappers.scrapper_edenred import EdenredScrapper
from scrappers.scrapper import Scrapper

bot_config = load_bot_config()


def get_scrappers() -> list[Scrapper]:
    scrappers = [
        MBWayScrapper(),
        OpenBankScrapper(),
        EdenredScrapper()
    ]

    # shuffling to avoid making requests at the exact same time every day
    random.shuffle(scrappers)
    return scrappers


def handle_exception(scrapper: Scrapper, e: Exception):
    trace = traceback.format_exc()
    print(trace)
    print(f"{datetime.now().time()}: failed getting discounts\n")

    if e is not ConnectionError:
        handle_error(bot_config, f"Error updating {scrapper.source} discounts: {trace}")


def main():
    old_discounts = load_discounts_from_file()
    updated_discounts = old_discounts.copy()

    scrappers = get_scrappers()
    count = 0

    for scrapper in scrappers:
        try:
            discounts = scrapper.get_discounts()
            discount_group = DiscountGroup(scrapper.source, discounts)
            count += len(discounts)

            # if there are no discounts, we assume something went wrong, so we keep the old ones
            if discounts:
                if discount_group in updated_discounts:
                    index = updated_discounts.index(discount_group)
                    updated_discounts[index] = discount_group
                else:
                    updated_discounts.append(discount_group)
            else:
                handle_error(bot_config, f"No {scrapper.source} discounts found, keeping previous ones if any")
        except KeyboardInterrupt:
            return
        except Exception as e:
            handle_exception(scrapper, e)

    print(f"{datetime.now().time()}: Total - got {count} discounts\n")
    save_discounts_to_file(updated_discounts)


if __name__ == "__main__":
    main()
