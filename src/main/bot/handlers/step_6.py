from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder

from src.config import settings
from src.main.bot.fsm.course_states import CourseStates
from src.main.bot.keyboards.main import (
    setup_testimonials_keyboard,
)
from src.main.utils.template import render_template

router = Router()


@router.callback_query(F.data == "ready_for_review", StateFilter(CourseStates.STEP_5))
async def step_6_handler(callback: CallbackQuery, state: FSMContext):
    """
    Отправляет предложение на персонализированный разбор.
    """
    await state.set_state(CourseStates.STEP_6)
    with suppress(TelegramBadRequest):
        step_6_message = render_template("6_step.html")
        image_ids: dict = settings.bot.images_dict["images"]["group"]
        album_builder = MediaGroupBuilder()
        await add_image_id(album_builder, image_ids)
        await callback.message.answer_media_group(media=album_builder.build())
        await callback.message.answer(
            text=step_6_message,
            reply_markup=await setup_testimonials_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()


async def add_image_id(album_builder, image_ids):
    for i in range(len(image_ids)):
        album_builder.add_photo(media=image_ids[f"photo_{i + 1}"])
