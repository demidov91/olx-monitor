import time
from updater import Updater
import logging

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    while True:
        try:
            logger.info('Start update.')
            Updater().update_news()
            logger.info('End update.')
            time.sleep(540)
        except:
            logger.exception('Unexpected exception')
            time.sleep(10)
