import asyncio
import logging
import random

from aiogram import types

from bot.misc import dp, redis
from bot.utils import get_photo_from_message
from config.settings import settings
from schemas import Image
from utils.serializers import ImageRedisSerializer
from bot.misc import bot

logger = logging.getLogger(__name__)

@dp.message_handler(
    commands=['help', 'start', 'about'],
)
async def handle_esthetique_photo(message: types.Message):

    logger.info(f'got command {message.text} from {message.from_user.id}')
    await message.answer(
        'Hello, I am esthetique bot, I work with only 1 chat.\n'
        'Any suggestions or issues, please open issue or PR:\n'
        'https://github.com/AlcibiadesCleinias/esthetique-telegram-bot',
    )
