from typing import List

from pydantic import BaseModel, validator
from datetime import datetime, timezone


class LikesBase(BaseModel):
    chat_id: int
    start: datetime = datetime.now(timezone.utc).isoformat()
    end: datetime = datetime.now(timezone.utc).isoformat()


class LikesIn(LikesBase):

    @validator('start', 'end', pre=True)
    def parse_date(cls, value):
        return datetime.fromisoformat(value)


class LikeStats(BaseModel):
    message_id: int
    like_2: int
    like_1: int
    like0: int
    like1: int
    like2: int


class LikesOut(LikesBase):
    likes_statistics: List[LikeStats]
