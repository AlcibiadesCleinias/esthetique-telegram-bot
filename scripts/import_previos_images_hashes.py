# I suppose this script to be an initial point for the stack
# since the script do next:
# - creates session for chat_history (telethon) in redis
# - goes through previous images and stores its hashes
#   fast (without http conversation b/w microservices)
#
# Requirement:
# - the group is a supergroup
# - chat history for new members is visible before a telethon user and a bot added
# - you know a chat id. E.g. after adding bot to chat check
#   via https://api.telegram.org/bot<UR TOKEN>/getUpdates
#   and prepared .env accordingly.
# - install python_dotenv==0.19.2
#
# Note:
# - to run script you have to install packages from both services:
#   chat_history and bot and you run the one from scripts/.
# - in script there is a bunch of hacks and tricky imports order.
# todo: ask bot for password (as well: add admin to bot)
# todo: Dockerfile for script? entrypoint?
import sys  # noqa
from io import BytesIO
from datetime import datetime

import aioredis
from pydantic import BaseSettings
from telethon import TelegramClient
from dotenv import load_dotenv
load_dotenv('../deploy/.env')  #  noqa

sys.path.append('../chat_history/src')  # noqa
from telegram.utils import is_esthetique_image_message_format
from telegram.client import session

sys.path.append('../bot/src')  # noqa  # todo: path order imports
from utils.serializers import ImageRedisSerializer
from schemas import Image


class CombinedSettings(BaseSettings):
    """Settings from both apps."""

    # chat_history settings
    TG_SESSION: str = 'telegram_session'
    TG_API_HASH: str
    TG_API_ID: int
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    # bot settings
    TG_BOT_ESTHETIQUE_CHAT: int

    class Config:
        case_sensitive = True


settings = CombinedSettings()

redis = aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', db=0)
client = TelegramClient(session, settings.TG_API_ID, settings.TG_API_HASH)


async def import_all_image_hashes_from_chat():
    me = await client.get_me()
    username = me.username
    print(f'U logged as {username}')

    entity = await client.get_entity(settings.TG_BOT_ESTHETIQUE_CHAT)

    messages = client.iter_messages(entity, offset_date=datetime(2007, 1, 1), reverse=True)  # return my 2007, pls
    async for message in messages:

        if is_esthetique_image_message_format(message):
            f = await message.download_media(file=bytes)
            f_bytesio = BytesIO(f)

            image = Image.construct(message_id=message.id, file=f_bytesio)  # hack with image
            serializer = ImageRedisSerializer(redis=redis, image=image)

            duplicate = await serializer.get_duplicate()
            if not duplicate:
                print(f'Photo from {message.id = } saved.')
                await serializer.save()
            else:
                print(f'{message.id = } has {duplicate = }. Pass it.')


def main():
    with client:
        client.loop.run_until_complete(import_all_image_hashes_from_chat())


if __name__ == '__main__':
    main()
