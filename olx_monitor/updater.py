import asyncio
import logging
from functools import partial

from aiohttp import ClientSession, TCPConnector
import os
from telegram import Bot, InputMediaPhoto
from telegram.error import RetryAfter

from olx_monitor.decorators import async_retry
from olx_monitor.tg_handler import TgHandler
from olx_monitor.db import subscription_collection, update_active_connection

logger = logging.getLogger(__name__)


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
            if record['id'] in subsription['seen']:
                continue

            await self.notify(subsription['chat_id'], record)
            await self.subscriptions.update_one(
                {'_id': subsription['_id']},
                {
                    '$push': {
                        'seen': {
                            '$each': [record['id']],
                            '$slice': -200,
                        },
                    },
                },
            )

    async def bulk_update(self, client: ClientSession, chat_id: int):
        """ Push all new ids into db in one go and build one message for all new links.
        :return: str or None
        """
        subscription = await subscription_collection().find_one({'chat_id': chat_id})
        data = [x for x in (await self._get_data(client, subscription)) if x['id'] not in subscription['seen']]

        if not data:
            return

        text = '\n\n'.join(*[build_basic_message(x) for x in data])

        await self.subscriptions.update_one(
            {'_id': subscription['_id']},
            {
                '$push': {
                    'seen': {
                        '$each': [x['id'] for x in data],
                        '$slice': -200,
                    },
                },
            },
        )

        return text

    async def _get_data(self, client: ClientSession, subscription: dict):
        response = await client.get(subscription['api_url'], timeout=30)
        return (await response.json())['data']

    @async_retry(retry_count=4, log_args=[1])
    async def notify(self, chat_id: int, record: dict):
        basic_message = build_basic_message(record)
        photos = [x['link'].replace(';s={width}x{height}', '') for x in record['photos']]
        if len(photos) == 0:
            await tg_retry_aware(partial(self.bot.send_message, chat_id, text=basic_message))

        elif len(photos) == 1:
            await tg_retry_aware(
                partial(self.bot.send_message, chat_id, text=f'{photos[0]}\n\n{basic_message}')
            )

        else:
            if len(photos) > 10:
                message = basic_message + '\n(więcej dostępnych zdjęć)'
            else:
                message = basic_message

            media = [InputMediaPhoto(x) for x in photos[:10]]
            media[0].caption = message
            await tg_retry_aware(partial(self.bot.send_media_group, chat_id, media=media))


async def tg_retry_aware(func):
    try:
        func()
    except RetryAfter as e:
        logger.info('Slow down %ss.', e.retry_after)
        await asyncio.sleep(e.retry_after)
        func()


def build_basic_message(olx_record: dict):
    is_promo = olx_record.get('promotion', {}).get('top_ad')
    title = olx_record['title']
    url = olx_record['url']
    promo_intro = "*Reklama\n" if is_promo else ""
    params = {x['key']: x['value'].get('label') for x in olx_record['params']}

    return f'{promo_intro}{title}\n\n{params.get("price")} + {params.get("rent")}\n\n{url}'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('').addHandler(TgHandler())

    async def _run():
        update_active_connection()
        await Updater().update_news()

    try:
        asyncio.run(_run())
    except Exception as e:
        logger.exception('Unexpected error: %s', e)
