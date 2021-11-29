from io import BytesIO

from aiogram.types import Message


async def get_photo_from_message(message: Message) -> BytesIO:
    file = BytesIO()
    await message.photo[-1].download(destination_file=file)
    return file
