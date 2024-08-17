from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from src.config import settings
from src.main.bot.keyboards.main import (
    setup_gift_discount_keyboard,
)
from src.main.utils.template import render_template
from src.main.bot.fsm.course_states import CourseStates

router = Router()


@router.callback_query(F.data == "view_reviews", StateFilter(CourseStates.STEP_6))
async def step_7_handler(callback: CallbackQuery, state: FSMContext):
    """
    Отправляет отзывы и результаты клиентов.
    """
    await state.set_state(CourseStates.STEP_7)
    step_7_message = render_template("7_step.html")
    await callback.message.answer_photo(
        photo=settings.bot.images_dict["images"]["photo_7"],
        caption=step_7_message,
        reply_markup=await setup_gift_discount_keyboard(),
    )
    await callback.answer()
