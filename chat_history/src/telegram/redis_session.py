import logging
from typing import Optional
from telethon.sessions import StringSession
import redis

logger = logging.getLogger(__name__)

# TODO: why string session is not async?
class RedisStringSession(StringSession):
    def __init__(self, session_id: str,redis_connector: redis.Redis):
        super().__init__()
        self.redis_connector = redis_connector
        self.session_id = session_id
        self.session_string = self._load()
        super().__init__(self.session_string)

    def get_session_redis_key(self) -> str:
        return f'session:{self.session_id}'

    def save(self):
        logger.info(f'Saving session to redis: {self.get_session_redis_key()}')

        session_string = super().save()
        self.redis_connector.set(self.get_session_redis_key(), session_string)

    def _load(self) -> Optional[str]:
        logger.info(f'Loaded session from redis: {self.get_session_redis_key()}')
        return self.redis_connector.get(self.get_session_redis_key())
