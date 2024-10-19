import datetime
import json
import logging
from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder
from yookassa import Payment, Configuration

from src.config import settings
from src.main.bot.fsm.payment_states import PaymentStates
from src.main.bot.keyboards.main import (
    setup_payment_keyboard,
    setup_prepayment_keyboard,
    setup_succeeded_payment_keyboard,
)
from src.main.bot.middlewares.users import UserMiddleware, SetupUserEmail
from src.main.utils.payment import DATA_CATEGORIES, create_payment
from src.main.utils.template import render_template

# Логирование успешных оплат
log_filename = "logs/payments.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_filename, encoding="UTF-8")],
)

router = Router()
Configuration.account_id = settings.bot.account_id
Configuration.secret_key = settings.bot.payments_token

router.message.middleware(UserMiddleware())
router.callback_query.middleware(SetupUserEmail())


@router.message(F.text.in_(DATA_CATEGORIES.keys()))
async def step_10_handler(message: Message, state: FSMContext):
    """
    Отправляет предложение о разборе по специальной цене, генерирует ссылку на оплату.
    """
    await state.set_state(PaymentStates.PAYMENT_START)
    await state.update_data(current_service=message.text)
    current_category = DATA_CATEGORIES[message.text]
    step_10_message = render_template(
        "10_step.html", settings.bot.price_list_dict[current_category]
    )
    image_ids: dict = settings.bot.images_dict["images"][current_category]
    album_builder = MediaGroupBuilder()
    await add_image_id(album_builder, image_ids)
    await message.answer_media_group(media=album_builder.build())

    data = await state.get_data()
    email = data.get("email")
    if not email:
        await message.answer(
            text=step_10_message,
            reply_markup=await setup_prepayment_keyboard(),
            parse_mode="HTML",
        )
    else:
        amount, description, payment_id, payment_url, step_10_1_message = (
            await setup_payment(data, email, message)
        )
        logging.info(
            f"Создан платеж: {payment_id}, пользователь: {message.from_user.username}, сумма: {amount}"
        )
        await message.answer(
            text=step_10_1_message,
            reply_markup=await setup_payment_keyboard(payment_url, payment_id),
            parse_mode="HTML",
        )


@router.callback_query(F.data == "get_email")
async def payment_start_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    with suppress(TelegramBadRequest):
        email = data.get("email")
        if not email:
            await state.set_state(PaymentStates.EMAIL)
            need_email_text = render_template("email.html")
            await callback.message.edit_text(
                text=need_email_text,
                parse_mode="HTML",
            )
        else:
            amount, description, payment_id, payment_url, step_10_1_message = (
                await setup_payment(data, email, callback.message)
            )
            logging.info(
                f"Создан платеж: {payment_id}, пользователь: {callback.from_user.username}, сумма: {amount}"
            )
            await callback.message.edit_text(
                text=step_10_1_message,
                reply_markup=await setup_payment_keyboard(payment_url, payment_id),
                parse_mode="HTML",
            )


async def setup_payment(data, email, message):
    current_category = DATA_CATEGORIES[data["current_service"]]
    step_10_1_message = render_template(
        "10_1_step.html", settings.bot.price_list_dict[current_category]
    )
    course_data = settings.bot.price_list_dict[current_category]
    amount = course_data["prices"]["standard"] - course_data["prices"]["discount"]
    # amount = 10
    description = f"Покупка через @ezo_tema_bot: {course_data['name']}, пользователь: @{message.from_user.username}"
    payment_url, payment_id = create_payment(
        amount=amount,
        chat_id=message.chat.id,
        email=email,
        description=description,
    )
    return amount, description, payment_id, payment_url, step_10_1_message


async def add_image_id(album_builder, image_ids):
    for i in range(len(image_ids)):
        album_builder.add_photo(media=image_ids[f"photo_{i + 1}"])


@router.callback_query(F.data.startswith("check_"))
async def check_payment_callback(
    callback: CallbackQuery,
    state: FSMContext,
):
    await callback.answer()
    payment_id = callback.data.split("_")[-1]
    payment = json.loads((Payment.find_one(payment_id)).json())
    with suppress(TelegramBadRequest):
        if payment and payment["status"] == "succeeded":
            logging.info(
                f"Оплата успешна: {payment['description']} Время: {datetime.datetime.now()}"
            )
            await state.set_state(PaymentStates.PAYMENT_SUCCEEDED)
            succeeded_payment_text = render_template("succeeded_payment.html")
            await callback.message.edit_media(
                media=InputMediaPhoto(
                    media=settings.bot.images_dict["images"]["photo_10"],
                    caption=succeeded_payment_text,
                ),
                reply_markup=await setup_succeeded_payment_keyboard(),
            )
        elif payment and payment["status"] == "pending":
            payment_url = payment["confirmation"]["confirmation_url"]
            await callback.message.edit_media(
                media=InputMediaPhoto(
                    media=settings.bot.images_dict["images"]["error"],
                    caption=render_template(
                        "check_payment.html", payment_id=payment_id
                    ),
                    parse_mode="HTML",
                ),
                reply_markup=await setup_payment_keyboard(payment_url, payment_id),
            )
            logging.info(
                f"Проверка платежа: {payment['description']} id платежа: {payment_id}",
            )
        else:
            await state.set_state(PaymentStates.PAYMENT_PASSED)
            await callback.message.edit_media(
                media=InputMediaPhoto(
                    media=settings.bot.images_dict["images"]["error"],
                    caption="Ошибка оплаты или срок действия ссылки истек. Попробуйте снова или обратитесь к "
                    "@mary_ezotema.",
                    parse_mode="HTML",
                ),
            )
