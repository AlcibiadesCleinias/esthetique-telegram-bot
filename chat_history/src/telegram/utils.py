from telethon.tl.custom import Message
import base64

from config.logger import get_app_logger

logger = get_app_logger()


def is_esthetique_image_message_format(message: Message) -> bool:
    """Check for a special message format,
    i.e. message is with image and 5 emoji buttons below created with tg-like bot.
    """

    buttons = message.buttons
    if not buttons:
        return False

    if not buttons or not isinstance(buttons, list):
        return False

    if not isinstance(buttons[0], list) or not len(buttons[0]) == 5:
        return False

    if not message.photo:
        return False

    return True


async def get_like_statistics_from_tg_message(message: Message) -> dict:
    """Extract like statistics from emoji buttons below the tg message with image."""

    emoji_like = {
        u'😡': 'like_2',
        u'😔': 'like_1',
        u'😐': 'like0',
        u'☺️': 'like1',
        u'😍': 'like2',
    }
    like_stats = {like_type: 0 for like_type in emoji_like.values()}

    for button in message.buttons[0]:  # todo: telethon hardcode
        texts = button.text.split()
        emoji_type = texts[0]

        if emoji_type not in emoji_like:
            logger.debug(f'{emoji_type} is not count..')
            continue

        if len(texts) == 2:
            try:
                like_stats[emoji_like[emoji_type]] += int(texts[1])
            except ValueError:
                logger.debug(f'Can not get int from text: {texts}. Pass...')
                pass

    return like_stats


async def get_base64_image_from_tg_message(message: Message) -> dict:
    """Get encoded with base64 image from message."""

    file = await message.download_media(file=bytes)
    return {'file': base64.b64encode(file)}
