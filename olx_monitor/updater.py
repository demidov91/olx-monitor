import asyncio
import logging
import re
from functools import partial
from typing import List
from urllib import parse

from aiohttp import ClientSession, TCPConnector
import os
from telegram import Bot, InputMediaPhoto
from telegram.error import BadRequest, RetryAfter, Forbidden

from olx_monitor.decorators import async_retry
from olx_monitor.tg_handler import TgHandler
from olx_monitor.db import subscription_collection, update_active_connection
from olx_monitor.constants import (
    MAX_PHOTOS_TO_SEND, SPACE_OLX_PARAM, PRICE_OLX_PARAM, ROOMS_OLX_PARAM, RENT_OLX_PARAM, MAX_OFFERS_TO_KEEP_IN_DB,
)

logger = logging.getLogger(__name__)

WANNA_PATTERN = re.compile('wann\w', flags=re.IGNORECASE)

class Updater:
    def __init__(self):
        self.subscriptions = subscription_collection()
        self.bot = Bot(os.environ['TG_TOKEN'])

    async def update_news(self):
        subs = [x async for x in self.subscriptions.find({'active': True})]

        async with ClientSession(connector=TCPConnector(limit=1)) as client:
            results = await asyncio.gather(
                *[self.process_subscription(client, x) for x in subs],
                return_exceptions=True
            )

        for data, res in zip(subs, results):
            if isinstance(res, Exception):
                logger.error("chat_id %s is not updated due to %s", data.get('chat_id'), res)

    async def process_subscription(self, client: ClientSession, subsription: dict):
        data = await self._get_data(client, subsription)

        for record in data:
            successfully_notified = await self.notify(subsription['chat_id'], record)
            if not successfully_notified:
                if (await self.deactivate(subsription['chat_id'])):
                    return

            else:
                await self.subscriptions.update_one(
                    {'_id': subsription['_id']},
                    {
                        '$push': {
                            'seen': {
                                '$each': [record['id']],
                                '$slice': -MAX_OFFERS_TO_KEEP_IN_DB,
                            },
                        },
                    },
                )

    async def bulk_update(self, client: ClientSession, chat_id: int):
        """ Push all new ids into db in one go and build one message for all new links.
        :return: str or None
        """
        subscription = await subscription_collection().find_one({'chat_id': chat_id})
        data = await self._get_data(client, subscription)

        if not data:
            return

        text = '\n\n'.join([build_basic_message(x) for x in data])

        await self.subscriptions.update_one(
            {'_id': subscription['_id']},
            {
                '$push': {
                    'seen': {
                        '$each': [x['id'] for x in data],
                        '$slice': -MAX_OFFERS_TO_KEEP_IN_DB,
                    },
                },
            },
        )

        return text

    async def _get_data(self, client: ClientSession, subscription: dict) -> List[dict]:
        all_records = await get_relevant_news(client, subscription['api_url'])
        new_records = [x for x in all_records if x['id'] not in subscription['seen']]
        records_to_show = [x for x in new_records if not is_promo_record(x)]
        if not records_to_show:
            return []

        # Add one promo record.
        for record in new_records:
            if is_promo_record(record):
                records_to_show.insert(0, record)
                break

        return records_to_show

    @async_retry(retry_count=4, log_args=[1])
    async def notify(self, chat_id: int, record: dict) -> bool:
        basic_message = build_basic_message(record)
        photos = [x['link'].replace(';s={width}x{height}', '') for x in record['photos']]
        if len(photos) == 0:
            await tg_retry_aware(partial(self.bot.send_message, chat_id, text=basic_message))

        elif len(photos) == 1:
            await tg_retry_aware(
                partial(self.bot.send_message, chat_id, text=f'{photos[0]}\n\n{basic_message}')
            )

        else:
            if len(photos) > MAX_PHOTOS_TO_SEND:
                message = basic_message + '\n(więcej dostępnych zdjęć)'
            else:
                message = basic_message

            media = [InputMediaPhoto(x) for x in photos[:MAX_PHOTOS_TO_SEND]]
            with media[0]._unfrozen():
                media[0].caption = message
            try:
                await tg_retry_aware(partial(self.bot.send_media_group, chat_id, media=media, read_timeout=20))
            except BadRequest as e:
                all_photos_in_one = '\n'.join(photos)
                logger.exception(
                    f'Failed to send {len(media)} photos with error message [{e.message}]\n'
                    f'Photos:\n{all_photos_in_one}'
                )
            except Forbidden:
                return False

        return True

    async def deactivate(self, chat_id) -> bool:
        await self.subscriptions.update_one(
            {'chat_id': chat_id},
            {'$set': {'active': False}},
        )
        logger.info('User %s will be deactivated.', chat_id)
        try:
            await self.bot.send_message(chat_id, text='...')
        except Forbidden:
            logger.info('User %s has been successfully deactivated.', chat_id)
            return True

        else:
            await self.subscriptions.update_one(
                {'chat_id': chat_id},
                {'$set': {'active': True}},
            )
            try:
                await self.bot.send_message(
                    chat_id,
                    text='Будь ласка, натисніть /stop якщо ви більш не жадаєте отримувати оновлення.',
                )
            except Forbidden:
                pass

            return False


async def tg_retry_aware(func):
    try:
        await func()
    except RetryAfter as e:
        logger.info('Slow down %ss.', e.retry_after)
        await asyncio.sleep(e.retry_after + 3)  # We don't hurry, can wait more.
        await func()


async def get_relevant_news(client, api_url: str):
    """Query remote data. Always consider total price when price limitation is specified."""
    _max_price_param = 'filter_float_price:to'
    _min_price_param = 'filter_float_price:from'
    records = (await (await client.get(api_url, timeout=30)).json())['data']

    parsed_url = parse.urlparse(api_url)
    all_query_params = parse.parse_qs(parsed_url.query)
    if _min_price_param in all_query_params or _max_price_param in all_query_params:
        min_price = float((all_query_params.get(_min_price_param) or [0])[0])
        max_price = float((all_query_params.get(_max_price_param) or ['inf'])[0])
        records = [x for x in records if is_relevant_olx_record(x, min_price, max_price)]

    return records


def is_relevant_olx_record(record: dict, min_price: float, max_price: float):
    params = get_record_params(record)
    total_price = str_to_price(params.get(PRICE_OLX_PARAM, '')) + str_to_price(params.get(RENT_OLX_PARAM, ''))
    return min_price <= total_price <= max_price

def str_to_price(str_price: str):
    m = re.search('([\d\s]+)', str_price)
    if m is None:
        return 0

    return float(re.sub('\s', '', m.group(1)))


def build_basic_message(olx_record: dict):
    is_promo = is_promo_record(olx_record)
    title = olx_record['title']
    url = olx_record['url']
    promo_intro = "*Reklama\n" if is_promo else ""
    params = get_record_params(olx_record)

    if params.get(RENT_OLX_PARAM) is not None:
        price_part = f'{params.get(PRICE_OLX_PARAM)} + {params[RENT_OLX_PARAM]}'
    else:
        price_part = f'Cena: {params.get(PRICE_OLX_PARAM)}'

    living_space_parts = [params[x] for x in (SPACE_OLX_PARAM, ROOMS_OLX_PARAM) if params.get(x) if not None]
    if WANNA_PATTERN.search(olx_record['description']) is not None:
        living_space_parts.append('🛁')

    living_space_part = ', '.join(living_space_parts)

    location_parts = (olx_record['location'].get(x, {}).get('name') for x in ('city', 'district'))
    location_part = ', '.join(x for x in location_parts if x is not None)

    return f'{promo_intro}{title}\n\n{price_part}\n{living_space_part}\n{location_part}\n\n{url}'


def get_record_params(olx_record: dict) -> dict:
    return {x['key']: x['value'].get('label') for x in olx_record['params']}



def is_promo_record(olx_record):
    return olx_record.get('promotion', {}).get('top_ad')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('').addHandler(TgHandler())

    async def _run():
        try:
            update_active_connection()
            await Updater().update_news()
        except Exception as e:
            logger.exception('Unexpected error: %s', e)
        finally:
            print('Wait 5 seconds to complete any tasks.')
            await asyncio.sleep(5)

    asyncio.run(_run())
