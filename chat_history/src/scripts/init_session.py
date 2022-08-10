"""Script helps you to craete session in redis once.
TODO: use callback with bot texting, e.g. await client.start(phone=phone,  code_callback=code_callback)
e.g. make telethon ask bot for pin in admin chat.
"""
from telethon import TelegramClient

from config.settings import settings
from telegram.client import session

client = TelegramClient(session, settings.TG_API_ID, settings.TG_API_HASH)


async def get_me():
    me = await client.get_me()
    print(f'U logged as {me.username}')


def main():
    with client:
        client.loop.run_until_complete(get_me())


if __name__ == '__main__':
    main()
