from fastapi import APIRouter

import schemas
from telegram.chat_history import get_likes_history, get_images_history


router = APIRouter()


@router.post('/likes', response_model=schemas.LikesOut)
async def get_likes_statistics(likes_in: schemas.LikesIn):
    likes = await get_likes_history(chat_id=likes_in.chat_id, start=likes_in.start, end=likes_in.end)
    return schemas.LikesOut.construct(likes_statistics=likes, **likes_in.dict())


# Deprecated coz for first cache heat we should use manage script.
# And aiogram has skip_updates arg.
@router.post(
    '/images',
    description=(
        'Get esthetique encoded with base64 images [bytes].\n'
        'Esthetique means message with 5 emoji/like buttons created via tg-like bot.'
    ),
    response_model=schemas.ImagesOut,
)
async def get_esthetique_images(like_images_in: schemas.ImagesIn):
    images = await get_images_history(
        chat_id=like_images_in.chat_id,
        start=like_images_in.start,
        end=like_images_in.end,
    )
    return schemas.ImagesOut.construct(images=images, **like_images_in.dict())
