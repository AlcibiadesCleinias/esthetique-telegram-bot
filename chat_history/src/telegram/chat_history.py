from datetime import datetime
from typing import List, Union, Callable, Type

from config.logger import get_app_logger
from schemas import Image, LikeStats
from telegram.client import bot_init
from telegram.utils import get_like_statistics_from_tg_message, is_esthetique_image_message_format, \
    get_base64_image_from_tg_message

logger = get_app_logger()


async def _get_esthetique_data_from_message_history(
        chat_id: int,
        start: datetime,
        end: datetime,
        returning_data_class: Union[Type[LikeStats], Type[Image]],
        extrac_function: Callable,
) -> List[Union[LikeStats, Image]]:

    async with await bot_init() as bot:
        entity = await bot.get_entity(chat_id)

        messages = bot.iter_messages(entity, offset_date=start, reverse=True)
        result = []
        async for message in messages:
            if message.date > end:
                logger.debug(f'We still have at least 1 message, but we reached the end {end}')
                break

            if not is_esthetique_image_message_format(message):
                logger.debug(f'Skip message {message.id} dut to not estatic format.')
                continue

            try:
                extract_result = await extrac_function(message)
            except (ValueError, IndexError) as e:
                logger.debug(f'Skip message  {message.id} due to error: {e}.')
                continue

            result.append(returning_data_class(message_id=message.id, **extract_result))

        return result


async def get_likes_history(chat_id: int, start: datetime, end: datetime) -> List[LikeStats]:
    """Get statistics of likes from images with emojis in bottom since the start.
    We used to create such images with like-tg bot.
    """

    return await _get_esthetique_data_from_message_history(
        chat_id, start, end, LikeStats, get_like_statistics_from_tg_message,
    )


async def get_images_history(chat_id: int, start: datetime, end: datetime) -> List[Image]:
    return await _get_esthetique_data_from_message_history(
        chat_id, start, end, Image, get_base64_image_from_tg_message,
    )
