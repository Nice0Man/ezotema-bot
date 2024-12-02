from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InputMediaPhoto,
    LinkPreviewOptions,
)

from src.config import settings
from src.main.bot.fsm.course_states import CourseStates
from src.main.bot.keyboards.main import setup_gift_guide_keyboard, setup_topic_keyboard
from src.main.bot.middlewares.subscription_check import SubscriptionCheckMiddleware
from src.main.utils.template import render_template

router = Router()

router.callback_query.middleware(SubscriptionCheckMiddleware())


@router.callback_query(F.data.startswith("is_"), StateFilter(CourseStates.STEP_3))
async def step_4_handler(callback: CallbackQuery, state: FSMContext):
    """
    Отправляет ссылку на гайд после подтверждения подписки.
    """
    await callback.answer()
    await state.set_state(CourseStates.STEP_4)
    with suppress(TelegramBadRequest):
        guide_key = callback.data.split(":")[-1]
        guide_link = settings.bot.gift_dict.get(guide_key)["url"]
        guide_name = settings.bot.gift_dict.get(guide_key)["name"]

        step_4_message = render_template(
            "4_step.html", guide_link=guide_link, guide_name=guide_name
        )
        await callback.message.answer_photo(
            photo=settings.bot.images_dict["images"]["photo_4"],
            caption=step_4_message,
            reply_markup=await setup_gift_guide_keyboard(),
        )


@router.callback_query(F.data.startswith("guide_"), StateFilter(CourseStates.STEP_3))
async def step_4_handler_other_buttons_not_subscribed(callback: CallbackQuery):
    """
    Отправляет ссылку на гайд после подтверждения подписки.
    """
    await callback.answer("Необходимо проверить подписку на канал, секундочку... ⌛")


@router.callback_query(F.data.startswith("guide_"), StateFilter(CourseStates.STEP_4))
async def step_4_handler_other_buttons(callback: CallbackQuery):
    """
    Отправляет ссылку на гайд после подтверждения подписки.
    """
    await callback.answer()
    with suppress(TelegramBadRequest):
        guide_key = callback.data.split(":")[-1]
        guide_link = settings.bot.gift_dict.get(guide_key)["url"]
        guide_name = settings.bot.gift_dict.get(guide_key)["name"]
        step_4_message = render_template(
            "4_1_step.html",
            guide_link=guide_link,
            guide_name=guide_name,
        )
        await callback.message.edit_text(
            text=step_4_message,
            parse_mode="HTML",
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=await setup_topic_keyboard(),
        )
