import time
from run import update_news
import logging

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    while True:
        try:
            logger.info('Start update.')
            update_news()
            logger.info('End update.')
            time.sleep(540)
        except:
            logger.exception('Unexpected exception')
