from enum import Enum

import aiohttp
from datetime import datetime

from config.logger import get_app_logger
from schemas import Likes

logger = get_app_logger()


async def _post_request(url, data) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=data) as response:
            try:
                return await response.json()
            except ValueError as e:
                logger.exception(f'Error {e} for {url = }: {response.text = }')
                raise e


class TgChatHistoryClient:  # todo: use session instead of simple request and control retry politics
    class Method(Enum):
        LIKES = 'likes'

    def __init__(self, chat_id: int, endpoint: str = 'http://localhost:8000/api/v1/esthetique/'):
        self.endpoint = endpoint
        self.chat_id = chat_id

    async def get_esthetique_stats(self, start: datetime, end: datetime) -> Likes:
        raw = await _post_request(
            self.endpoint + self.Method.LIKES.value,
            data={
                'chat_id': self.chat_id,
                'start': start.isoformat(),
                'end': end.isoformat(),
            },
        )
        return Likes(**raw)
