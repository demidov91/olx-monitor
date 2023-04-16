import logging
import os
from traceback import print_exc
import asyncio

from telegram import Bot


class TgHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        if 'level' not in kwargs:
            kwargs['level'] = logging.ERROR

        self.bot = Bot(os.environ['TG_TOKEN'])
        super().__init__(*args, **kwargs)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            asyncio.run(self.bot.send_message(chat_id=os.environ['ADMIN_ID'], text=record.message))
        except:
            print("Can't use TgHandler due to the following error.")
            print_exc()