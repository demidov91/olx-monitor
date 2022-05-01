import asyncio

from olx_monitor.tg_handler import TgHandler
from olx_monitor.updater import Updater
import logging

logger = logging.getLogger(__name__)


async def infinite_loop():
    while True:
        try:
            logger.info('Start update.')
            await Updater().update_news()
            logger.info('End update.')
            await asyncio.sleep(540)

        except asyncio.CancelledError:
            raise

        except Exception:
            logger.exception('Unexpected exception')
            await asyncio.sleep(10)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('').addHandler(TgHandler())
    asyncio.run(infinite_loop())
