from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder

from src.config import settings
from src.main.bot.keyboards.main import setup_start_keyboard
from src.main.utils.template import render_template
from src.main.bot.fsm.course_states import CourseStates

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(CourseStates.START)
    welcome_message = render_template("1_step.html")
    inline_keyboard = await setup_start_keyboard()
    await message.answer_photo(
        photo=settings.bot.images_dict["images"]["photo_1"],
        caption=welcome_message,
        reply_markup=inline_keyboard,
    )


@router.callback_query(StateFilter(CourseStates.IDLE))
async def answer_topic_handler(callback: CallbackQuery):
    await callback.answer("Вы уже перешли на следующий шаг. ✨")
