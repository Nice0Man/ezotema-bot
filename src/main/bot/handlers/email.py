from contextlib import suppress
import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from email_validator import validate_email

from src.config import settings
from src.main.bot.fsm.payment_states import PaymentStates
from src.main.bot.handlers.payment import setup_payment, check_payment, create_payment
from src.main.bot.keyboards.main import setup_payment_keyboard
from src.main.bot.middlewares.users import AddUserMiddleware
from src.main.utils.template import render_template

router = Router()

router.message.middleware(AddUserMiddleware)


@router.message(
    F.text.cast(validate_email).normalized.as_("email"),
    StateFilter(PaymentStates.EMAIL),
)
async def get_email_handler(
    message: Message,
    state: FSMContext,
    email: str,
):
    await state.set_state(PaymentStates.PAYMENT_PENDING)
    await state.update_data(email=email)
    data = await state.get_data()
    with suppress(TelegramBadRequest):
        amount, description, payment_id, payment_url, step_10_1_message = (
            await setup_payment(data, email, message)
        )
        await message.answer_photo(
            photo=settings.bot.images_dict["images"]["photo_9"],
            caption=step_10_1_message,
            reply_markup=await setup_payment_keyboard(payment_url, payment_id),
            parse_mode="HTML",
        )
        payment = await check_payment(payment_id, 60, state)
        if payment["status"] != "succeeded":
            passed_payment_text = render_template("passed_payment_text.html")
            payment_url, payment_id = create_payment(
                amount=amount,
                chat_id=message.chat.id,
                email=email,
                description=description,
            )
            logging.info(
                f"Создан повторный платеж: {payment_id}, пользователь: {message.from_user.username}, сумма: {amount}"
            )
            await message.answer(
                text=passed_payment_text,
                parse_mode="HTML",
                reply_markup=await setup_payment_keyboard(payment_url, payment_id),
            )


@router.message(StateFilter(PaymentStates.EMAIL))
async def get_invalid_email_handler(message: Message):
    await message.answer("Пожалуйста, введите корректный адрес электронной почты.")
