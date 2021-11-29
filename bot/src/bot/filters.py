from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from bot.misc import dp


class EsthetiqueFormatFilter(BoundFilter):
    key = 'is_esthetique_format'

    def __init__(self, is_esthetique_format: bool = True):
        self.is_esthetique_format = is_esthetique_format

    async def check(self, message: types.Message):
        if not (
                message.photo and message.reply_markup and message.reply_markup.inline_keyboard
                and isinstance(message.reply_markup.inline_keyboard[0], list)
        ):
            return False is self.is_esthetique_format

        return bool(len(message.reply_markup.inline_keyboard[0]) == 5) is self.is_esthetique_format


dp.filters_factory.bind(EsthetiqueFormatFilter)
