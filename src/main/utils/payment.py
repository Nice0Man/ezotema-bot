import asyncio
import json

from aiogram.fsm.context import FSMContext
from yookassa import Payment

from src.main.bot.fsm.payment_states import PaymentStates

DATA_CATEGORIES: dict = {
    "👸Women's Club": "women_s_club",
    "🌙Натальная карта": "natal_chart",
    "✨Матрица судьбы": "matrix_of_fate",
    "👑Полный разбор": "full_analysis",
    "🧝🏻‍♀️Разбор стиля": "style_analysis",
    "💞Отношения (ПОЛНЫЙ гайд)": "relationship_analysis",
    "🌟Разбор одного положения": "one_position_analysis",
    "🐱Детская матрица": "children_matrix",
    "💍Совместимость": "compatibility",
}


def create_payment(
    amount: int,
    chat_id: str,
    email: str,
    description: str,
) -> dict:
    """
    Создание платежа через yookassa.
    :param email:
    :param chat_id:
    :param amount: Сумма платежа
    :param description: Описание платежа

    """
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

    return payment.confirmation.confirmation_url, payment.id


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
