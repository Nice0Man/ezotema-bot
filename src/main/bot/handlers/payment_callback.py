from aiogram import F
from aiogram.types import CallbackQuery

from .payment import router
from src.main.bot.keyboards.main import PaymentCallbackData


@router.callback_query(PaymentCallbackData.filter(F.action == "pay"))
async def process_payment_callback(
    callback_query: CallbackQuery, callback_data: PaymentCallbackData
):
    await callback_query.answer()
    await callback_query.message.answer(
        f"Processing payment for ID: {callback_data.payment_id}"
    )


# Callback handler for cancellation
@router.callback_query(PaymentCallbackData.filter(F.action == "cancel"))
async def process_cancel_callback(
    callback_query: CallbackQuery, callback_data: PaymentCallbackData
):
    await callback_query.answer()
    await callback_query.message.answer(
        f"Subscription cancelled for ID: {callback_data.payment_id}"
    )


# Callback handler for checking payment
@router.callback_query(PaymentCallbackData.filter(F.action == "check"))
async def process_check_callback(
    callback_query: CallbackQuery, callback_data: PaymentCallbackData
):
    await callback_query.answer()
    await callback_query.message.answer(
        f"Checking payment status for ID: {callback_data.payment_id}"
    )
