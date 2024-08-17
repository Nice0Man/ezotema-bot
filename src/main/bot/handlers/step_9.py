from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.main.bot.fsm.course_states import CourseStates
from src.main.bot.keyboards.main import setup_reply_session_keyboard
from src.main.utils.template import render_template

router = Router()


@router.callback_query(F.data == "get_session", StateFilter(CourseStates.STEP_8))
async def step_8_handler(callback: CallbackQuery, state: FSMContext):
    """
    Отправляет предложение о разборе по специальной цене.
    """
    await state.set_state(CourseStates.STEP_9)
    step_9_message = render_template("9_step.html")
    await callback.message.answer(
        text=step_9_message, reply_markup=await setup_reply_session_keyboard()
    )
    await callback.answer()
