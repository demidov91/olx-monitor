from requests import Session
import pymongo
import os
from telegram import Bot


db_client = pymongo.MongoClient(os.environ['DB_CONNSTRING'])
subscriptions = db_client['olx-monitor']['subscription']
bot = Bot(os.environ['TG_TOKEN'])


def __main__():
    with Session() as client:
        for subscription in subscriptions.find({}):
            process_subscription(client, subscription)


def process_subscription(client: Session, subsription: dict):
    data = client.get(subsription['api_url'], timeout=30).json()['data']

    for record in data:
        if record['id'] in subsription['seen']:
            continue

        notify(subsription['chat_id'], record)
        subscriptions.update_one({'_id': subsription['_id']}, {'$push': {'seen': record['id']}})


def notify(chat_id: int, record: dict):
    photo_url = record["photos"][0]["link"]
    photo_url = photo_url.replace(';s={width}x{height}', '')

    msg = f'{photo_url}\n\n{record["title"]}\n\n{record["url"]}'

    bot.send_message(chat_id, text=msg)


if __name__ == '__main__':
    __main__()





