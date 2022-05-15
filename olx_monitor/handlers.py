from olx_monitor.exceptions import UnexpectedUrlFormat
from olx_monitor.url_interpreter import browser_url_to_api
from olx_monitor.db import subscription_collection


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

    return '✅'


async def stop_updates(chat_id):
    await subscription_collection().update_one(
        {'chat_id': chat_id},  # create an index!
        {'$set': {'active': False}},
        upsert=False,
    )

    return '\U0001f6d1'
