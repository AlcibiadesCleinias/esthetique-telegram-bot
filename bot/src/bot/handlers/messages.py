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


async def _duplicate_warn(chat_id: int, sender_id: int, sender_message_id: int, original_message_id: int):
    async def _bro():
        await bot.send_message(
            chat_id=chat_id,
            text=f'Hey, {sender_id}, bro, seems you duplicated this one',
            reply_to_message_id=original_message_id,
        )

    async def _stickerochek():
        await bot.send_sticker(
            chat_id=chat_id,
            sticker=random.choice([
                'CAACAgIAAx0CYy9UggADMGGkOdn5_lKMm0v2lBEG8XbLTwJHAAIzAAPYahYQBqWljQKJdpAiBA',
                'CAACAgIAAx0CYy9UggADM2GkOm85app0Wx1Xqypok7l_IH6kAAI0AAPYahYQKdZ6LYBoGIkiBA',
                'CAACAgIAAx0CYy9UggADNGGkOn-wZfdx4gNuG3uTLVZyraX_AAI6AAPYahYQflbGPWwW2VoiBA',
                'CAACAgIAAx0CYy9UggADNWGkOpiMSXPwNYNjtPOKZMu1nKJVAAI7AAPYahYQhe2Te5NF-mEiBA',
                'CAACAgIAAx0CYy9UggADNmGkOq7pTv4TnoX2A771WwUnAAEWsQACHwAD2GoWEDAFXgn-vPZ4IgQ',
                'CAACAgIAAx0CYy9UggADN2GkOvSGoYiGxxZ_L_z25mhmQa1jAAIeAAPYahYQueCh9mNLrzEiBA',
                'CAACAgIAAx0CYy9UggADPWGkPaH7jqm0cFhM6KRhSf61pttsAAINAwACEzmPEWPVqCB_X-3SIgQ',  # boi
                'CAACAgQAAx0CYy9UggADPmGkPcCpun-P3W_iMhWeqwfaX45MAAITMgACw4FiCcvUltlN1aeaIgQ',  # angry cat
                'CAACAgQAAx0CYy9UggADP2GkPeuyBpKjMvnEHl7wteqDRjvDAAJnMgACw4FiCVXDFX7LffiiIgQ',  # sniff
            ]),
            reply_to_message_id=sender_message_id,
        )
        await bot.send_message(
            chat_id=chat_id,
            text='.',
            reply_to_message_id=original_message_id,
        )

    await random.choices([_bro, _stickerochek], [0.15, 0.85])[0]()


@dp.message_handler(
    content_types=['photo'],
    chat_id=settings.TG_BOT_ESTHETIQUE_CHAT,
    is_esthetique_format=True,
)
async def handle_esthetique_photo(message: types.Message):
    logging.info(f'[handle_esthetique_photo] {message = }')

    image_file = await get_photo_from_message(message)
    image = Image(message_id=message.message_id, file=image_file)
    image_serialier = ImageRedisSerializer(image=image, redis=redis)

    async with asyncio.Lock():
        duplicated_message_id = await image_serialier.get_duplicate()
        if not duplicated_message_id:
            logger.info(f'New esthetique came from {message.from_user}, remember photo hash...')
            return await image_serialier.save()

        logger.info(
            f'{message.from_user} sent duplicate with {message.message_id} '
            f'of {duplicated_message_id}. Warn him...'
        )
        await _duplicate_warn(
            message.chat.id,
            message.from_user.mention,
            message.message_id,
            duplicated_message_id,
        )
