import os
from urllib.parse import urljoin
from aiohttp import web

import logging

from telegram import Update

from olx_monitor.db import update_active_connection
from olx_monitor.handlers import handle_browser_url, stop_updates
from olx_monitor.tg_handler import TgHandler
from olx_monitor.url_interpreter import like_an_url_pattern
from olx_monitor.constants import HELP_MESSAGE

logger = logging.getLogger(__name__)


def build_url(base_url):
    return urljoin(base_url, urljoin('olx_monitor', os.environ['SECURE_URL']))


def build_tg_message(text:str, chat_id: int):
    if text:
        return {
            'method': 'sendMessage',
            'text': text,
            'chat_id': chat_id,
        }

    return None


async def handle_update(request):
    update_active_connection()
    try:
        return web.json_response(await root_handler(request))
    except:
        logger.exception('Unexpected error is silenced.')
        return web.Response()


async def root_handler(request):
    tg_update = Update.de_json(await request.json(), None)
    if not tg_update.effective_user:
        return {}

    if not tg_update.message.text:
        return

    chat_id = tg_update.effective_chat.id

    if like_an_url_pattern.match(tg_update.message.text):
        return build_tg_message(
            await handle_browser_url(tg_update.message.text, chat_id),
            chat_id=chat_id,
        )

    if tg_update.message.text == '/stop':
        return build_tg_message(await stop_updates(chat_id), chat_id=chat_id)

    if tg_update.message.text == '/help':
        return build_tg_message(HELP_MESSAGE, chat_id=chat_id)


async def init(argv):
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('').addHandler(TgHandler())

    app = web.Application()
    app.router.add_post(build_url('/'), handle_update)
    return app
