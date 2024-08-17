from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from src.config import settings
from src.main.bot.keyboards.main import (
    setup_personal_review_keyboard,
)
from src.main.utils.template import render_template
from src.main.bot.fsm.course_states import CourseStates

router = Router()


@router.callback_query(F.data == "get_gift", StateFilter(CourseStates.STEP_4))
async def step_5_handler(callback: CallbackQuery, state: FSMContext):
    """
    Отправляет подарок — лекцию на основе выбранной темы.
    """
    await state.set_state(CourseStates.STEP_5)
    with suppress(TelegramBadRequest):
        gift_message = render_template("5_step.html")  # Лекция для других тем
        await callback.message.answer_photo(
            photo=settings.bot.images_dict["images"]["photo_5"],
            caption=gift_message,
            reply_markup=await setup_personal_review_keyboard(),
        )
        await callback.answer()
