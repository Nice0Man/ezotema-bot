from aiogram.fsm.state import StatesGroup, State


class PaymentStates(StatesGroup):
    PAYMENT_SUCCEEDED = State()
    PAYMENT_PASSED = State()
    PAYMENT_PENDING = State()
    EMAIL = State()
    PAYMENT_GET_EMAIL = State()
    PAYMENT_START = State()
