import os
from telegram import Bot


def set_webhook():
    bot = Bot(os.environ['TG_TOKEN'])
    print(bot.set_webhook('https://2644-37-30-104-111.ngrok.io'))


if __name__ == '__main__':
    set_webhook()



