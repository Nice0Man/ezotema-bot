import asyncio
import json

from aiogram.fsm.context import FSMContext
from yookassa import Payment
from yookassa.domain.response import PaymentResponse

from src.main.bot.fsm.payment_states import PaymentStates

# Constants
NATAL_CHART = "🌙Натальная карта"
WOMEN_S_CLUB = "👸Women's Club"
MATRIX_OF_FATE = "✨Матрица судьбы"
FULL_ANALYSIS = "👑Полный разбор"
STYLE_ANALYSIS = "🧝🏻‍♀️Разбор стиля"
RELATIONSHIP_ANALYSIS = "💞Отношения (ПОЛНЫЙ гайд)"
ONE_POSITION_ANALYSIS = "🌟Разбор одного положения"
CHILDREN_MATRIX = "🐱Детская матрица"
COMPATIBILITY = "💍Совместимость"
WISH_CARD = "🧡Гайд Карта Желаний "

EZOTEMA_ERROR_MESSAGE = (
    "Ошибка оплаты или срок действия ссылки истек. Попробуйте снова или обратитесь к "
    "@mary_ezotema."
)

DATA_CATEGORIES: dict = {
    WOMEN_S_CLUB: "women_s_club",
    NATAL_CHART: "natal_chart",
    MATRIX_OF_FATE: "matrix_of_fate",
    FULL_ANALYSIS: "full_analysis",
    STYLE_ANALYSIS: "style_analysis",
    RELATIONSHIP_ANALYSIS: "relationship_analysis",
    ONE_POSITION_ANALYSIS: "one_position_analysis",
    CHILDREN_MATRIX: "children_matrix",
    COMPATIBILITY: "compatibility",
    WISH_CARD: "wish_card",
}


def create_payment(
    amount: int,
    chat_id: str,
    email: str,
    description: str,
    save_payment_method: bool,
) -> PaymentResponse:
    """
    Создание платежа через yookassa.
    :param save_payment_method: Метод оплаты
    :param email:
    :param chat_id:
    :param amount: Сумма платежа
    :param description: Описание платежа

    """

    if save_payment_method:
        payment = Payment.create(
            {
                "amount": {
                    "value": amount,
                    "currency": "RUB",
                },
                "confirmation": {
                    "type": "embedded",
                    "confirmation_token": "",
                    "return_url": "https://t.me/ezo_tema_bot",
                },
                "capture": True,
                "description": description,
                "save_payment_method": save_payment_method,
                "metadata": {
                    "chat_id": chat_id,
                },
                "receipt": {
                    "customer": {
                        "email": email,
                    },
                    "items": [
                        {
                            "description": description,
                            "quantity": "1.00",
                            "amount": {
                                "value": amount,
                                "currency": "RUB",
                            },
                            "vat_code": "1",
                            "payment_mode": "full_payment",
                            "payment_subject": "service",
                        },
                    ],
                },
            }
        )
    else:
        payment = Payment.create(
            {
                "amount": {
                    "value": amount,
                    "currency": "RUB",
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://t.me/ezo_tema_bot",
                },
                "capture": True,
                "description": description,
                "save_payment_method": save_payment_method,
                "metadata": {
                    "chat_id": chat_id,
                },
                "receipt": {
                    "customer": {
                        "email": email,
                    },
                    "items": [
                        {
                            "description": description,
                            "quantity": "1.00",
                            "amount": {
                                "value": amount,
                                "currency": "RUB",
                            },
                            "vat_code": "1",
                            "payment_mode": "full_payment",
                            "payment_subject": "service",
                        },
                    ],
                },
            }
        )
    return payment


async def check_payment(payment_id: str, sleep_seconds: int, state: FSMContext):
    payment = json.loads((Payment.find_one(payment_id)).json())
    n = 0
    tmp_state = await state.get_state()
    if tmp_state == PaymentStates.PAYMENT_PASSED:
        return None
    elif tmp_state == PaymentStates.PAYMENT_SUCCEEDED:
        return payment
    while (payment["status"] == "pending" or n > 40) and tmp_state:
        payment = json.loads((Payment.find_one(payment_id)).json())
        await asyncio.sleep(sleep_seconds)  # Pause before checking again
        n += 1
    return payment
