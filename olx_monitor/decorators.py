import asyncio
import logging
from functools import partial, wraps


logger = logging.getLogger(__name__)


def async_retry(coro=None, retry_count=None, initial_wait_time=10, log_args=()):
    if coro is None:
        return partial(async_retry, retry_count=retry_count, initial_wait_time=initial_wait_time, log_args=log_args)

    @wraps(coro)
    async def wrapper(*args, **kwargs):
        for retry_counter in range(retry_count + 1):
            if retry_counter > 0:
                # First iteration.
                logger.info(
                    'Trying to restart %s%s. %s/%s',
                    coro,
                    tuple(args[x] for x in log_args),
                    retry_counter,
                    retry_count,
                )

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
                    'Error (%s) while running %s%s. Restarting in %s seconds...',
                    e, coro.__name__, tuple(args[x] for x in log_args), wait_for_before_restart,
                    exc_info=True
                )

                await asyncio.sleep(wait_for_before_restart)

    return wrapper
