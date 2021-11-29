import logging

from config.settings import settings


def get_app_logger():
    return logging.getLogger(settings.LOGGER_NAME)
