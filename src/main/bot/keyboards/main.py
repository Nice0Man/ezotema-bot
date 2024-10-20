from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Клавиатура для 1-го шага
async def setup_start_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для приветственного шага.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Уже взял чай, рассказывай!☕️", callback_data="start_tea")
    return builder.adjust(1).as_markup()


# Клавиатура для 2-го шага (выбор темы)
async def setup_topic_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора темы на втором шаге.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Проявление", callback_data="guide_manifestation")
    builder.button(text="Финансы", callback_data="guide_finance")
    builder.button(text="Отношения", callback_data="guide_relationship")
    builder.button(text="Стиль", callback_data="guide_style")
    return builder.adjust(2).as_markup()


# Клавиатура для 3-го шага (подписка на канал)
async def setup_subscription_keyboard(prev_callback_name: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для проверки подписки на телеграм-канал.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Подписался на канал", callback_data=f"is_subscribed:{prev_callback_name}"
    )
    return builder.adjust(1).as_markup()


# Клавиатура для 4-го шага (получение гайда)
async def setup_gift_guide_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для получения гайда на четвертом шаге.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Получить подарок!", callback_data="get_gift")
    return builder.adjust(1).as_markup()


# Клавиатура для 5-го шага (получение подарка)
async def setup_personal_review_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора персонализированного разбора на шестом шаге.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Как? 📖", callback_data="ready_for_review")
    return builder.adjust(1).as_markup()


# Клавиатура для 7-го шага (просмотр отзывов)
async def setup_testimonials_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для просмотра отзывов клиентов на седьмом шаге.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Как проходит разбор? 💖", callback_data="view_reviews")
    return builder.adjust(1).as_markup()


# Клавиатура для 8-го шага (получение разбора по скидке)
async def setup_gift_discount_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для получения скидки на восьмом шаге.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Получить разбор по акции 🌈", callback_data="get_discount")
    return builder.adjust(1).as_markup()


# Клавиатура для 9-го шага (получение разбора по скидке)
async def setup_session_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для получения разбора на восьмом шаге.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Получить разбор! 📖", callback_data="get_session")
    return builder.adjust(1).as_markup()


async def setup_reply_session_keyboard() -> ReplyKeyboardMarkup:
    """
    Создание основной клавиатуры бота (ReplyKeyboardMarkup).
    """
    keyboard_buttons = [
        [
            KeyboardButton(text="🌙Натальная карта"),
            KeyboardButton(text="✨Матрица судьбы"),
        ],
        [
            KeyboardButton(text="👑Полный разбор"),
            KeyboardButton(text="🧝🏻‍♀️Разбор стиля"),
        ],
        [KeyboardButton(text="💞Отношения (ПОЛНЫЙ гайд)")],
        [KeyboardButton(text="🌟Разбор одного положения")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True)
    return keyboard


async def setup_prepayment_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить 💰", callback_data="get_email")
    return builder.adjust(1).as_markup()


async def setup_payment_keyboard(
    payment_url: str, payment_id: str
) -> InlineKeyboardMarkup:
    """
    Клавиатура для оплаты разборов на 10 шаге.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить 💸", url=payment_url)
    builder.button(text="Проверить оплату ✔️", callback_data=f"check_{payment_id}")
    return builder.adjust(1).as_markup()


async def setup_check_payment_keyboard(payment_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Проверить оплату ✔️", callback_data=f"check_{payment_id}")
    return builder.adjust(1).as_markup()


async def setup_succeeded_payment_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для оплаты разборов на 10 шаге.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Перейти в канал 🤗", url="https://t.me/ezo_tema")
    return builder.adjust(1).as_markup()
