import asyncio
import datetime
import logging
from functools import partial, wraps


logger = logging.getLogger(__name__)


def async_retry(coro=None, retry_count=None, initial_wait_time=10):
    if coro is None:
        return partial(async_retry, retry_count=retry_count, initial_wait_time=initial_wait_time)

    @wraps(coro)
    async def wrapper(*args, **kwargs):
        for retry_counter in range(retry_count + 1):
            if retry_counter > 0:
                # First iteration.
                logger.info('Trying to restart %s. %s/%s', coro, retry_counter, retry_count)

            try:
                return await coro(*args, **kwargs)
            except asyncio.CancelledError as e:
                raise

            except Exception as e:
                if retry_counter == (retry_count):
                    # Last iteration.
                    raise

                wait_for_before_restart = initial_wait_time * 2 ** retry_counter

                logger.warning(
                    'Error (%s) while running %s. Restarting in %s seconds...',
                    e, coro.__name__, wait_for_before_restart
                )

                await asyncio.sleep(wait_for_before_restart)

    return wrapper