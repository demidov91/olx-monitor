import os
from urllib.parse import urljoin
from aiohttp import web

import logging

from telegram import Update

from olx_monitor.db import update_active_connection
from olx_monitor.tg_handler import TgHandler
from olx_monitor.url_interpreter import like_an_url_pattern, browser_url_to_api
from olx_monitor.exceptions import UnexpectedUrlFormat

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

    if tg_update.message.text and like_an_url_pattern.match(tg_update.message.text):
        return build_tg_message(
            await tg_handle_browser_url(tg_update.message.text),
            chat_id=tg_update.effective_chat.id,
        )


async def tg_handle_browser_url(text: str):
    try:
        return browser_url_to_api(text)
    except UnexpectedUrlFormat as e:
        logger.error(str(e))
        return str(e)


async def init(argv):
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('').addHandler(TgHandler())

    app = web.Application()
    app.router.add_post(build_url('/'), handle_update)
    return app
