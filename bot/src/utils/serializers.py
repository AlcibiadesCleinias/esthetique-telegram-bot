from typing import Optional
from io import BytesIO

from redis.asyncio import Redis
from asyncio import Lock
from PIL import Image as PILImage
import imagehash
import numpy as np

from schemas import Image


class ImageRedisSerializer:
    """Serializer for telegram image with duplication check feature.
    On save we store key:value as hash:message_id.
    """

    def __init__(self, image: Image, redis: Redis):
        self.redis = redis
        self.image = image
        self._hash = None
        self._lock = Lock()

    async def get_duplicate(self) -> Optional[int]:
        """We return telegram message id of already saved image."""

        if not self._hash:
            self._hash = ImageRedisSerializer.calc_image_hash(self.image.file)

        stored = await self.redis.get(self._hash)
        return int(stored) if stored else stored

    async def save(self) -> int:
        """We return id of tg message saved."""

        if not self._hash:
            self._hash = ImageRedisSerializer.calc_image_hash(self.image.file)

        return await self.redis.set(self._hash, self.image.message_id)

    @staticmethod
    def calc_image_hash(image: BytesIO) -> str:
        _hash = imagehash.average_hash(PILImage.open(image), hash_size=32)
        h = ''.join(map(str, np.array(_hash.hash, dtype=int).reshape(-1)))
        return str(hex(int(h, 2)))
