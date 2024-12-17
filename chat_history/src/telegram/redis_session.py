import logging
from typing import Optional
from telethon.sessions import StringSession
import redis

logger = logging.getLogger(__name__)


# TODO: why string session is not async?
class RedisStringSession(StringSession):
    def __init__(self, session_id: str, redis_connector: redis.Redis):
        self.redis_connector = redis_connector
        self.session_id = session_id
        self.session_string = self.__load()
        super().__init__(self.session_string)

    def get_session_redis_key(self) -> str:
        return f'session:{self.session_id}'

    def save(self):
        session_string = super().save()
        self.redis_connector.set(self.get_session_redis_key(), session_string)

    def __load(self) -> Optional[str]:
        return self.redis_connector.get(self.get_session_redis_key())
