from telethon import TelegramClient
from teleredis import RedisSession  # todo: to async
from config.settings import settings
import redis  # todo: to async


redis_connector = redis.Redis(  # todo: relocate
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=False,
)
session = RedisSession(settings.TG_SESSION, redis_connector)


async def bot_init() -> TelegramClient:
    bot = TelegramClient(
        session=session,
        api_id=settings.TG_API_ID,
        api_hash=settings.TG_API_HASH,
    )

    return await bot.start()
