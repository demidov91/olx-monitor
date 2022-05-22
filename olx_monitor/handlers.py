import asyncio

from aiohttp import ClientSession

from olx_monitor.exceptions import UnexpectedUrlFormat
from olx_monitor.url_interpreter import browser_url_to_api
from olx_monitor.db import subscription_collection
from olx_monitor.updater import Updater
from olx_monitor.constants import HELP_MESSAGE

import logging
logger = logging.getLogger(__name__)


async def handle_browser_url(text: str, chat_id: int):
    try:
        api_url = browser_url_to_api(text)
    except UnexpectedUrlFormat as e:
        logger.error(str(e))
        return str(e)

    await subscription_collection().update_one(
        {'chat_id': chat_id},   # create an index!
        {'$set': {'api_url': api_url, 'browser_url': text, 'active': True}, '$setOnInsert': {'seen': []}},
        upsert=True,
    )

    mass_message = await bulk_update(chat_id)
    return mass_message or '✅'


async def bulk_update(chat_id: int):
    async with ClientSession() as client:
        return await Updater().bulk_update(client, chat_id)


async def stop_updates(chat_id):
    await subscription_collection().update_one(
        {'chat_id': chat_id},  # create an index!
        {'$set': {'active': False}},
        upsert=False,
    )

    return '\U0001f6d1'


async def tg_help(chat_id):
    record = await subscription_collection().find_one(
        {'chat_id': chat_id},
    )

    if record is None or not record.get('active'):
        active_filter_text = '❌ У вас зараз немає активних пошуків'

    else:
        active_filter = record.get('browser_url', 'unknown')
        active_filter_text = f'Активний пошук: {active_filter}'

    return HELP_MESSAGE.format(filter_message=active_filter_text)

