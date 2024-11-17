from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from src.config import settings
from src.main.bot.fsm.course_states import CourseStates
from src.main.bot.keyboards.main import setup_channel_subscription_keyboard
from src.main.utils.template import render_template

router = Router()


@router.callback_query(F.data.startswith("guide_"), StateFilter(CourseStates.STEP_2))
async def step_3_handler(callback: CallbackQuery, state: FSMContext):
    """
    Проверяет подписку на телеграм-канал и отправляет ссылку на канал.
    """
    await callback.answer()
    await state.set_state(CourseStates.STEP_3)
    step_3_message = render_template("3_step.html")

    await callback.message.answer_photo(
        photo=settings.bot.images_dict["images"]["photo_3"],
        caption=step_3_message,
        reply_markup=await setup_channel_subscription_keyboard(
            callback.data
        ),  # Кнопка для перехода на канал
    )
