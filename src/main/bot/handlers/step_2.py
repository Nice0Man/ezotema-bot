from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from src.main.bot.keyboards.main import setup_topic_keyboard
from src.main.utils.template import render_template
from src.main.bot.fsm.course_states import CourseStates

router = Router()


@router.callback_query(F.data == "start_tea", StateFilter(CourseStates.START))
async def step_2_handler(callback: CallbackQuery, state: FSMContext):
    """
    Отправляет сообщение со списком тем и запросом выбора.
    """
    await state.set_state(CourseStates.STEP_2)
    step_2_message = render_template("2_step.html")
    await callback.message.answer(
        text=step_2_message,
        reply_markup=await setup_topic_keyboard(),  # Клавиатура для выбора темы
    )
    await callback.answer()  # Необходимо завершить callback
