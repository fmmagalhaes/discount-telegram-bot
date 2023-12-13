import requests

# https://medium.com/codex/using-python-to-send-telegram-messages-in-3-simple-steps-419a8b5e5e2


def handle_error(bot_config, message):
    print(message)

    if "CHAT_ID" not in bot_config:
        return

    # let's handle the error by sending a message to the chat
    token = bot_config["TOKEN"]
    chat_id = bot_config["CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "disable_web_page_preview": True,
    }

    response = requests.post(url, json=payload).json()

    if response["ok"] is not True:
        error = response["description"]
        print(error)
        # if POST failed, let's send the error with GET - it's a more limited way of sending messages
        url = f"{url}?chat_id={chat_id}&text={error}"
        response = requests.get(url).json()
