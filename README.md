# Discount Telegram Bot

## Overview

Do you ever buy something, only to find later that you had a discount for it?  
This Python project is a Telegram bot that scrapes various sources for discounts and provides them to users on command.

The project consists of two main components:
- A discount updater script (`main_discount_updater.py`)
- The Telegram bot itself (`main_telegram_bot.py`).

## Installation

1. Clone the repository
2. Install the required dependencies ```pip install -r requirements.txt```
3. Setup your telegram bot with the [Bot Father](https://telegram.me/BotFather)
4. Copy `bot_template.yaml` to `bot.yaml` and modify the `TOKEN` and `CHAT_ID` values in `bot.yaml`
   1. If something goes wrong while collecting the discount from the sources, a message will be sent to that chat.
   2. If you don't want to be notified, simply remove `CHAT_ID` from `bot.yaml`
5. If you're on Linux, install the ChromeDriver driver with `sudo apt install chromium-chromedriver`

## Usage

### Discount Updater
Run the discount updater script to scrape discount information from the sources and generate a file with the results.

```python main_discount_updater.py```

You can set up a cronjob to run this script at regular intervals to keep the discount information up-to-date.

### Telegram Bot
Run the Telegram bot to provide users with discount information fetched from the generated file.

```python main_telegram_bot.py```

The bot responds to the following commands:

`/search`: Search for specific discounts  
`/all`: Retrieve all available discounts

<img src="https://github.com/fmmagalhaes/discount-telegram-bot/assets/8866496/834dd1e3-a0fe-449b-9c9b-e2a6050dfc99" height="500">

## Contributing
Feel free to contribute to the project by adding other sources of discount information.
