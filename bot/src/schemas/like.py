from typing import List

from pydantic import BaseModel


class LikeStats(BaseModel):
    message_id: int
    like_2: int
    like_1: int
    like0: int
    like1: int
    like2: int


class Likes(BaseModel):
    likes_statistics: List[LikeStats]
