# better to use aiocron? no
# better to use apschedulers? no
# -_-
import asyncio
import functools
from typing import Coroutine, Callable, Any, Tuple, Optional
from datetime import datetime

from croniter import croniter

from config.logger import get_app_logger

logger = get_app_logger()


async def _wait_until(dt: datetime):
    while True:
        now = datetime.now()
        remaining = (dt - now).total_seconds()
        if remaining < 86400:
            break
        await asyncio.sleep(86400)

    await asyncio.sleep(remaining)


async def cron_task(cron_expression: str, coro: Callable[..., Coroutine[Any, Any, Any]], base: datetime = None):
    """Simple double looped croniter (cron scheduler) to be register in running loop."""

    logger.info(f'Start task {coro}')

    if base is None:
        base = datetime.now()

    cron = croniter(cron_expression, base, ret_type=datetime, max_years_between_matches=15)
    next = cron.next()

    while True:
        await _wait_until(next)
        try:
            logger.info(f'Start executing {coro}...')
            await coro()
            logger.info(f'End executing {coro}.')
        except Exception as e:
            logger.exception(f'Could not proceed with {coro}: {e}. Pass it...')
        next = cron.next()


class CronTaskBase:
    """Hint: To run once you can call smth like loop.run_until_complete(CronTaskBase().coro())."""
    # todo: create decorator for __call__
    def __init__(
            self,
            cron_expression: Optional[str] = None,
            coro: Optional[Callable[..., Coroutine[Any, Any, Any]]] = None,
            args: Optional[Tuple] = (),
    ):
        self.cron_expression = cron_expression
        self.coro = coro if not args else functools.partial(coro, *args)

    def register(self):
        loop = asyncio.get_event_loop()
        loop.create_task(cron_task(self.cron_expression, self.coro))
