import asyncio

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.config import settings
from src.main.bot.fsm.course_states import CourseStates
from src.main.bot.keyboards.main import setup_topic_keyboard
from src.main.utils.template import render_template

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(CourseStates.START)
    welcome_message = render_template("1_step.html")
    await message.answer_photo(
        photo=settings.bot.images_dict["images"]["photo_1"],
        caption=welcome_message,
    )
    await asyncio.sleep(settings.skip.S1)
    await step_2_handler(message, state)


async def step_2_handler(message: Message, state: FSMContext):
    """
    Отправляет сообщение со списком тем и запросом выбора.
    """
    await state.set_state(CourseStates.STEP_2)
    step_2_message = render_template("2_step.html")
    await message.answer(
        text=step_2_message,
        reply_markup=await setup_topic_keyboard(),  # Клавиатура для выбора темы
    )


@router.callback_query(StateFilter(CourseStates.IDLE))
async def answer_topic_handler(callback: CallbackQuery):
    await callback.answer("Вы уже перешли на следующий шаг. ✨")
