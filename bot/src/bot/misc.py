import asyncio
import logging

import redis.asyncio
from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor

from config.settings import settings

logging.basicConfig(
    format=u'%(levelname)-8s | %(asctime)s | %(message)s | %(filename)+13s',
    level=settings.LOG_LEVEL,
)

# in code below it uses asyncio lock inside when creates connection pool
redis = redis.asyncio.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', db=0)
# storage = RedisStorage2(**REDIS_SETTINGS) if REDIS_SETTINGS else MemoryStorage()
loop = asyncio.get_event_loop()

bot = Bot(token=settings.TG_BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)  # , storage=storage)
executor = Executor(dp, skip_updates=settings.TG_BOT_SKIP_UPDATES)
