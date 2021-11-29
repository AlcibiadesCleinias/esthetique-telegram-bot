from pydantic import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str = 'INFO'
    LOGGER_NAME: str = 'app_logger'

    TG_BOT_TOKEN: str
    TG_BOT_SKIP_UPDATES: bool = True

    TG_BOT_ESTHETIQUE_CHAT: int
    TG_BOT_ESTHETIQUE_FIRST_BESTS: int = 10
    TG_BOT_ESTHETIQUE_STATS_CRON: str = '*/5 * * * *'

    REDIS_HOST: str
    REDIS_PORT: int = 6379

    TG_CHAT_HISTORY_APP_ENDPOINT: str = ''

    class Config:
        case_sensitive = True


settings = Settings()
