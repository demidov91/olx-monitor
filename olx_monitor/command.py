import os
from telegram import Bot


def set_webhook():
    bot = Bot(os.environ['TG_TOKEN'])
    # bot.set_webhook('')


if __name__ == '__main__':
    set_webhook()



