from pydantic import BaseModel
from io import BytesIO


class Image(BaseModel):
    message_id: int
    file: BytesIO

    class Config:
        arbitrary_types_allowed = True
