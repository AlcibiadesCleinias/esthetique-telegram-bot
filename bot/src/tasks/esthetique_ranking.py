import random
from datetime import datetime

from croniter import croniter
import numpy as np

from bot.misc import bot
from clients.telegram_chat_history import TgChatHistoryClient
from config.logger import get_app_logger
from config.settings import settings
from utils.calculations import calculate_weight
from utils.cron import CronTaskBase
from utils.time import now_utc

logger = get_app_logger()


async def _send_preambulo():
    async def _comes():
        await bot.send_message(
            settings.TG_BOT_ESTHETIQUE_CHAT,
            'Here he comes\n\n'.upper() * 3,
        )
        await bot.send_sticker(
            settings.TG_BOT_ESTHETIQUE_CHAT,
            'CAACAgIAAxkBAAMxZ19Qhb-2HwdFJUG9UPqInQSlAh4AAiptAALex_lKCB-WzhHJlHE2BA',
        )
        await bot.send_message(
            settings.TG_BOT_ESTHETIQUE_CHAT,
            'He has arrived'.upper(),
        )

    async def _info():
        await bot.send_message(
            settings.TG_BOT_ESTHETIQUE_CHAT,
            'Пора глянуть статистику...',
        )

    async def _thinking():
        await bot.send_sticker(
            settings.TG_BOT_ESTHETIQUE_CHAT,
            'CAACAgQAAx0CYy9UggADLWGkN7f_BKlzgK5cki7vFiQCA9vxAAKWAAPxhYsEIptHks6k0bEiBA',
        )
    await random.choice([_comes, _info, _thinking])()


async def _show_best_esthetiques(n):
    """Show first n best esthetiques since the date calculated with help of croniter,
    i.e. show in replays esthetique formatted messages with best stats.
    """

    end = now_utc().replace(second=0, microsecond=0)
    cron = croniter(settings.TG_BOT_ESTHETIQUE_STATS_CRON, start_time=end, max_years_between_matches=1)
    start = cron.get_prev(datetime)

    chat_history = TgChatHistoryClient(
        chat_id=settings.TG_BOT_ESTHETIQUE_CHAT,
        endpoint=settings.TG_CHAT_HISTORY_APP_ENDPOINT,
    )

    stats = await chat_history.get_esthetique_stats(start=start, end=end)
    if not stats.likes_statistics:
        logger.info(f"No statistic info comes for period: {start} - {end}")
        return

    sorted_indexes = np.argsort([calculate_weight(stat) for stat in stats.likes_statistics])
    sorted_indexes_first_n = sorted_indexes[len(sorted_indexes) - n:]

    await _send_preambulo()

    for position, likes_stats_idx in enumerate(sorted_indexes_first_n):
        like_stats = stats.likes_statistics[likes_stats_idx]
        await bot.send_message(
            settings.TG_BOT_ESTHETIQUE_CHAT,
            f'#{len(sorted_indexes_first_n) - position}',
            reply_to_message_id=like_stats.message_id,
        )


class ShowBestEsthetiquesTask(CronTaskBase):
    def __init__(self):
        super().__init__(
            settings.TG_BOT_ESTHETIQUE_STATS_CRON,
            coro=_show_best_esthetiques,
            args=(settings.TG_BOT_ESTHETIQUE_FIRST_BESTS,),
        )
