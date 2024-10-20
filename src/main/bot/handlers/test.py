from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder
from email_validator import validate_email

router = Router()


# @router.message(F.photo)
# async def handle_photo(message: Message):
#     # Get the largest photo version (highest resolution)
#     photo = message.photo[-1]
#     photo_id = photo.file_id
#
#     # Send the photo file_id back to the user
#     await message.answer(photo_id)
#     album_builder = MediaGroupBuilder(caption=photo_id)
#     album_builder.add_photo(media=photo_id)
#     await message.answer_media_group(media=album_builder.build())


# @router.message(
#     F.text.cast(validate_email).normalized.as_("email"),
# )
# async def get_email_handler(message: Message):
#     await message.answer(f"Your email is {message.text}")
