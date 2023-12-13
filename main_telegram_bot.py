import time
from common.discount import DiscountGroup
from common.file_manager import load_bot_config, load_discounts_from_file
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from unidecode import unidecode

MAX_CHARACTERS = 4096


async def send_discounts_message(update, context, discount_groups: list[DiscountGroup]):
    message = ""
    count = 0
    for group in discount_groups:
        for discount in group.discounts:
            count += 1
            message += f"#{count} {group.source}\n{discount.content}\n\n"

    if not count:
        message = "No discounts found :("

    chat_id = update.effective_chat.id
    for x in range(0, len(message), MAX_CHARACTERS):
        await context.bot.send_message(
            chat_id=chat_id, text=message[x:x+MAX_CHARACTERS], disable_web_page_preview=len(discount_groups) != 1, parse_mode="HTML")


async def search(update, context):
    print("Received request /search")
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="What are you looking for?")

    return 1


async def cancel(update, context):
    print("Received request /cancel")
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="Bye!")

    return ConversationHandler.END


async def all_discounts(update, context):
    print("Received request /all")
    discount_groups = get_discounts_from_file()
    await send_discounts_message(update, context, discount_groups)


async def get_discounts(update, context):
    word = update.message.text
    print(word)
    discount_groups = get_discounts_from_file(word)
    await send_discounts_message(update, context, discount_groups)

    return ConversationHandler.END


def get_discounts_from_file(word_filter: str = "") -> list[DiscountGroup]:
    discount_groups = load_discounts_from_file()

    if not word_filter:
        return discount_groups

    filtered_groups = []
    for group in discount_groups:
        group_discounts = []
        for discount in group.discounts:
            if unidecode(word_filter.lower()) in unidecode(discount.content.lower()):
                group_discounts.append(discount)

        if group_discounts:
            filtered_groups.append(DiscountGroup(
                group.source, group_discounts))

    return filtered_groups


def start_bot(bot_token):
    # https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#polling-vs-webhook
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("start", search))
    application.add_handler(CommandHandler("all", all_discounts))

    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("search", search)],
            states={
                1: [MessageHandler(filters.TEXT & (~ filters.COMMAND), get_discounts)]
            },
            fallbacks=[CommandHandler("cancel", cancel)]
        )
    )

    return application.run_polling(1)


def main():
    print("loading bot config...")
    bot_token = load_bot_config()["TOKEN"]

    print("starting bot...")
    max_retries = 10
    retry_interval = 20
    retries = 0

    while retries < max_retries:
        try:
            if retries >= 1:
                print("Retrying...")
            if start_bot(bot_token):
                print("Bot is listening!\n")
                break
            else:
                print("Something went wrong while starting the bot.")
        except Exception as e:
            print(f"Error: {e}\n")

        retries += 1

        if retries == max_retries:
            print("Max retries reached. Exiting...")

        time.sleep(retry_interval)


if __name__ == "__main__":
    main()
