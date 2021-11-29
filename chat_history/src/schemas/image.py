from typing import List
from pydantic import BaseModel, validator
from datetime import datetime, timezone


class ImagesBase(BaseModel):
    chat_id: int
    start: datetime = datetime.now(timezone.utc).isoformat()
    end: datetime = datetime.now(timezone.utc).isoformat()


class ImagesIn(ImagesBase):

    @validator('start', 'end', pre=True)
    def parse_date(cls, value):
        return datetime.fromisoformat(value)


class Image(BaseModel):
    message_id: int
    file: bytes


class ImagesOut(ImagesBase):
    images: List[Image]
