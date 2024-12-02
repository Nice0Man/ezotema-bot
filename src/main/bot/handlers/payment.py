import datetime
import json
import logging
from contextlib import suppress
from typing import Tuple, Dict, Any

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder
from email_validator import validate_email
from yookassa import Payment, Configuration

from src.config import settings
from src.main.bot.fsm.payment_states import PaymentStates
from src.main.bot.keyboards.main import (
    setup_base_payment_keyboard,
    setup_prepayment_keyboard,
    setup_succeeded_payment_keyboard,
    setup_membership_payment_keyboard,
)
from src.main.bot.middlewares.users import UserMiddleware, SetupUserEmail
from src.main.db.schemas.users import UserBase
from src.main.utils.payment import (
    DATA_CATEGORIES,
    create_payment,
    WOMEN_S_CLUB,
    EZOTEMA_ERROR_MESSAGE,
)
from src.main.utils.template import render_template, add_image_id


# Logger setup
def setup_logger() -> logging.Logger:
    logger_ = logging.getLogger(__name__)
    logger_.setLevel(logging.INFO)
    file_handler = logging.FileHandler("logs/payments.log", encoding="UTF-8")
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger_.addHandler(file_handler)
    return logger_


logger = setup_logger()

# Router setup
router = Router()
Configuration.account_id = settings.bot.account_id
Configuration.secret_key = settings.bot.payments_token

router.message.middleware(UserMiddleware())
router.callback_query.middleware(SetupUserEmail())


@router.message(F.text.in_(DATA_CATEGORIES.keys()))
async def step_10_handler(message: Message, state: FSMContext, user: UserBase):
    await state.set_state(PaymentStates.PAYMENT_START)
    await state.update_data(current_service=message.text)
    current_category = DATA_CATEGORIES[message.text]
    await send_media_group(message, current_category)
    await handle_payment_offer(message, state, user)


async def send_media_group(message: Message, category: str):
    image_ids: dict = settings.bot.images_dict["images"][category]
    album_builder = MediaGroupBuilder()
    await add_image_id(album_builder, image_ids)
    await message.answer_media_group(media=album_builder.build())


async def handle_payment_offer(message: Message, state: FSMContext, user: UserBase):
    data = await state.get_data()
    if not user.email:
        await message.answer(
            text=render_template(
                "10_step.html", settings.bot.price_list_dict[data["current_service"]]
            ),
            reply_markup=await setup_prepayment_keyboard(),
            parse_mode="HTML",
        )
    else:
        if message.text == WOMEN_S_CLUB:
            await process_membership_payment(message, state, user.email)
        else:
            await process_base_payment(message, state, user.email)


async def process_membership_payment(message: Message, state: FSMContext, email: str):
    data = await state.get_data()
    current_category = DATA_CATEGORIES[data["current_service"]]
    membership_subscription_message = render_template(
        "membership_subscription.html", settings.bot.price_list_dict[current_category]
    )
    course_data = settings.bot.price_list_dict[current_category]
    # amount = course_data["prices"]["standard"] - course_data["prices"]["discount"]
    amount = 5
    description = f"Покупка через @ezo_tema_bot: {course_data['name']}, пользователь: @{message.from_user.username}"
    payment_id, payment_token = await setup_payment(
        amount=amount,
        chat_id=message.chat.id,
        email=email,
        description=description,
    )
    logger.info(
        f"Создан платеж: {payment_id}, пользователь: {message.from_user.username}, сумма: {amount}"
    )
    await message.answer(
        text=membership_subscription_message,
        reply_markup=await setup_membership_payment_keyboard(payment_id),
        parse_mode="HTML",
    )


async def process_base_payment(message: Message, state: FSMContext, email: str):
    data = await state.get_data()
    current_category = DATA_CATEGORIES[data["current_service"]]
    step_10_1_message = render_template(
        "10_1_step.html", settings.bot.price_list_dict[current_category]
    )
    course_data = settings.bot.price_list_dict[current_category]
    amount = course_data["prices"]["standard"] - course_data["prices"]["discount"]
    description = f"Покупка через @ezo_tema_bot: {course_data['name']}, пользователь: @{message.from_user.username}"
    payment_id, payment_url = await setup_payment(
        amount=amount,
        chat_id=message.chat.id,
        email=email,
        description=description,
    )
    logger.info(
        f"Создан платеж: {payment_id}, пользователь: {message.from_user.username}, сумма: {amount}"
    )
    await message.answer(
        text=step_10_1_message,
        reply_markup=await setup_base_payment_keyboard(payment_url, payment_id),
        parse_mode="HTML",
    )


@router.message(
    F.text.cast(validate_email).normalized.as_("email"),
    StateFilter(PaymentStates.EMAIL),
)
async def get_email_handler(message: Message, state: FSMContext, email: str):
    await state.set_state(PaymentStates.PAYMENT_PENDING)
    await state.update_data(email=email)
    await process_base_payment(message, state, email)


@router.callback_query(F.data == "get_email")
async def payment_start_handler(
    callback: CallbackQuery, state: FSMContext, user: UserBase
):
    with suppress(TelegramBadRequest):
        email = user.email
        if not email:
            await request_email(callback, state)
        else:
            await process_base_payment(callback.message, state, email)


async def request_email(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PaymentStates.EMAIL)
    need_email_text = render_template("email.html")
    await callback.message.edit_text(
        text=need_email_text,
        parse_mode="HTML",
    )


async def setup_payment(
    amount: int,
    chat_id: str,
    email: str,
    description: str,
    save_payment_method: bool = False,
) -> Tuple[str, str]:
    """
    Sets up a payment and returns the payment URL and ID.

    :param save_payment_method:
    :param amount: The amount for the payment
    :param chat_id: The chat ID associated with the payment
    :param email: The email of the user making the payment
    :param description: The description of the payment
    :return: A tuple containing the payment URL and payment ID
    """
    payment = create_payment(
        amount=amount,
        chat_id=chat_id,
        email=email,
        description=description,
        save_payment_method=save_payment_method,
    )
    if not save_payment_method:
        return payment.id, payment.confirmation.confirmation_url
    else:
        return payment.id, payment.confirmation.confirmation_token


@router.callback_query(F.data.startswith("check_"))
async def check_payment_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    payment_id = callback.data.split("_")[-1]
    payment = json.loads((Payment.find_one(payment_id)).json())
    with suppress(TelegramBadRequest):
        print(payment)
        if payment and payment["status"] == "succeeded":
            await handle_successful_payment(callback, state, payment)
        elif payment and payment["status"] == "pending":
            await handle_pending_payment(callback, payment_id, payment)
        else:
            await handle_failed_payment(callback, state, payment_id)


async def handle_successful_payment(
    callback: CallbackQuery, state: FSMContext, payment: Dict[str, Any]
):
    logger.info(
        f"Оплата успешна: {payment['description']} Время: {datetime.datetime.now()}"
    )
    await state.set_state(PaymentStates.PAYMENT_SUCCEEDED)
    succeeded_payment_text = render_template("succeeded_payment.html")
    await edit_message_with_media(
        callback,
        succeeded_payment_text,
        "photo_10",
        await setup_succeeded_payment_keyboard(),
    )


async def handle_pending_payment(
    callback: CallbackQuery, payment_id: str, payment: Dict[str, Any]
):
    payment_url = payment["confirmation"]["confirmation_url"]
    check_payment_text = render_template("check_payment.html", payment_id=payment_id)
    await edit_message_with_media(
        callback,
        check_payment_text,
        "error",
        await setup_base_payment_keyboard(payment_url, payment_id),
    )
    logger.info(
        f"Проверка платежа: {payment['description']} id платежа: {payment_id}",
    )


async def handle_failed_payment(
    callback: CallbackQuery, state: FSMContext, payment_id: str
):
    await state.set_state(PaymentStates.PAYMENT_PASSED)
    await edit_message_with_media(callback, EZOTEMA_ERROR_MESSAGE, "error", None)
    logger.info(f"Ошибка оплаты id платежа: {payment_id}")


async def edit_message_with_media(
    callback: CallbackQuery, text: str, image_key: str, reply_markup: Any
):
    if callback.message.photo:
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=settings.bot.images_dict["images"][image_key],
                caption=text,
                parse_mode="HTML",
            ),
            reply_markup=reply_markup,
        )
    else:
        await callback.message.edit_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
