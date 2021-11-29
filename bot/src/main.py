from aiogram import Dispatcher

from bot.misc import executor
# note, that line below is very convenience and meaningful
from bot import filters, handlers  # noqa
from tasks.esthetique_ranking import ShowBestEsthetiquesTask
from config.logger import get_app_logger

logger = get_app_logger()


async def on_startup(dp: Dispatcher):
    logger.info('Start the bot...')


async def on_shutdown(dp: Dispatcher):
    logger.info('Stopping the bot...')


def main():
    ShowBestEsthetiquesTask().register()

    executor.on_startup(on_startup, polling=0)
    executor.on_shutdown(on_shutdown, polling=0)
    executor.start_polling()


if __name__ == '__main__':
    main()
