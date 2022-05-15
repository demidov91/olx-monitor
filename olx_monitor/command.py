import os
from telegram import Bot
import sys
import json
import urllib.request
from itertools import chain
from olx_monitor.constants import CITIES_URL, DATA_DIR
from olx_monitor.server import build_url

import logging
logger = logging.getLogger(__name__)


def set_webhook(url: str):
    bot = Bot(os.environ['TG_TOKEN'])
    url_to_set = build_url(url)
    print(url_to_set)
    print(bot.set_webhook(url_to_set))


def get_webhook():
    bot = Bot(os.environ['TG_TOKEN'])
    return bot.get_webhook_info()


def build_region(region: dict):
    logger.info('Get cities %s %s.', region['id'], region['normalized_name'])
    region_cities = json.load(urllib.request.urlopen(CITIES_URL.format(region_id=region['id'])))['data']
    for city in region_cities:
        city['region-id'] = region['id']
        city['region-normalized_name'] = region['normalized_name']

    return region_cities


def build_cities():
    with open(os.path.join(DATA_DIR, 'regions.json'), 'rt') as f:
        regions = json.load(f)

    all_cities = chain(*[build_region(x) for x in regions])

    with open(os.path.join(DATA_DIR, 'cities.json'), 'wt') as f:
        json.dump({x.pop('normalized_name'): x for x in all_cities}, f, indent=2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    if sys.argv[1] == 'set_webhook':
        set_webhook(sys.argv[2])

    elif sys.argv[1] == 'build_cities':
        build_cities()

    elif sys.argv[1] == 'get_webhook':
        print(get_webhook())

