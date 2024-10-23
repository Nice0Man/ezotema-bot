from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from src.config import settings
from src.main.bot.keyboards.main import setup_reply_session_keyboard
from src.main.utils.template import add_image_id

router = Router()


@router.message(Command("analyse"))
async def analyse_command_handler(message: Message):
    await message.answer(
        text="⭐ Жми на кнопочку и выбирай! ⭐",
        reply_markup=await setup_reply_session_keyboard(),
    )


@router.message(Command("reviews"))
async def analyse_command_handler(message: Message):
    image_ids: dict = settings.bot.images_dict["images"]["reviews"]
    album_builder = MediaGroupBuilder(caption="Скорее ознакомься с отзывами! ❤️")
    await add_image_id(album_builder, image_ids)
    await message.answer_media_group(media=album_builder.build())
