from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.config import settings
from src.main.bot.fsm.course_states import CourseStates
from src.main.bot.keyboards.main import (
    setup_session_keyboard,
)
from src.main.utils.template import render_template

router = Router()


@router.callback_query(F.data == "get_discount", StateFilter(CourseStates.STEP_7))
async def step_8_handler(callback: CallbackQuery, state: FSMContext):
    """
    Отправляет предложение о разборе по специальной цене.
    """
    await state.set_state(CourseStates.STEP_8)
    step_8_message = render_template("8_step.html")
    await callback.message.answer_photo(
        photo=settings.bot.images_dict["images"]["photo_8"],
        caption=step_8_message,
        reply_markup=await setup_session_keyboard(),
    )
    await callback.answer()
