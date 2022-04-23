from requests import Session
import pymongo
import os
from telegram import Bot, InputMediaPhoto


class Updater:
    def __init__(self):
        _db_client = pymongo.MongoClient(os.environ['DB_CONNSTRING'])
        self.subscriptions = _db_client['olx-monitor']['subscription']
        self.bot = Bot(os.environ['TG_TOKEN'])

    def update_news(self):
        with Session() as client:
            for subscription in self.subscriptions.find({}):
                self.process_subscription(client, subscription)

    def process_subscription(self, client: Session, subsription: dict):
        data = client.get(subsription['api_url'], timeout=30).json()['data']

        for record in data:
            if record['id'] in subsription['seen']:
                continue

            self.notify(subsription['chat_id'], record)
            self.subscriptions.update_one({'_id': subsription['_id']}, {'$push': {'seen': record['id']}})

    def notify(self, chat_id: int, record: dict):
        is_promo = record.get('promotion', {}).get('top_ad')
        title = record['title']
        url = record['url']

        photos = [x['link'].replace(';s={width}x{height}', '') for x in record['photos']]
        promo_intro = "*Reklama\n" if is_promo else ""
        params = {x['key']: x['value'].get('label') for x in record['params']}

        basic_message = f'{promo_intro}{title}\n\n{params.get("price")} + {params.get("rent")}\n\n{url}'

        if len(photos) == 0:
            self.bot.send_message(chat_id, text=basic_message)

        elif len(photos) == 1:
            self.bot.send_message(chat_id, text=f'{photos[0]}\n\n{basic_message}')

        else:
            if len(photos) > 10:
                message = basic_message + '\n(więcej dostępnych zdjęć)'
            else:
                message = basic_message

            media = [InputMediaPhoto(x) for x in photos[:10]]
            media[0].caption = message
            self.bot.send_media_group(chat_id, media=media)


if __name__ == '__main__':
    Updater().update_news()





