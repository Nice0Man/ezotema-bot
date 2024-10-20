import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message, CallbackQuery

from src.main.bot.fsm.payment_states import PaymentStates
from src.main.db.crud import users as user_crud
from src.main.db.schemas.users import UserCreate, UserUpdate
from src.main.utils.db_helper import db_helper


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> None:
        user_id = event.from_user.id
        username = event.from_user.username
        chat_id = event.chat.id
        email = None
        state: FSMContext = data.get("state")
        if state:
            state_data = await state.get_data()
            email = state_data.get("email")
        async with db_helper.session_factory() as session:
            existing_user = await user_crud.get_user_by_id(session, user_id)
        if existing_user:
            data["user"] = existing_user
            logging.info(
                f"Пользователь найден в базе данных: "
                f"ID={user_id}, "
                f"username={existing_user.username}, "
                f"email={existing_user.email}"
            )
        else:
            new_user = UserCreate(
                id=user_id, username=username, email=email, chat_id=chat_id
            )
            async with db_helper.session_factory() as session:
                await user_crud.create_user(session, new_user.dict())
            data["user"] = new_user
            logging.info(
                f"Новый пользователь добавлен: ID={user_id}, username={username}, email={email}"
            )
        result = await handler(event, data)
        return result


class SetupUserEmail(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> None:
        user_id = event.from_user.id
        username = event.from_user.username
        chat_id = event.message.chat.id
        state: FSMContext = data.get("state")
        async with db_helper.session_factory() as session:
            existing_user = await user_crud.get_user_by_id(session, user_id)
        if existing_user:
            data["user"] = existing_user
            if existing_user.email:
                pass
            else:
                if state:
                    state_data = await state.get_data()
                    email = state_data.get("email")
                    if email:
                        user_update = UserUpdate(
                            email=email, username=username, chat_id=chat_id
                        )
                        async with db_helper.session_factory() as session:
                            await user_crud.update_user(
                                session,
                                user_id=user_id,
                                update_data=user_update.dict(),
                            )
                        logging.info(
                            f"Добавлена почта: {email} для пользователя: ID={user_id}, username={username}"
                        )
                        data["user"] = existing_user
                    else:
                        await state.set_state(PaymentStates.EMAIL)
                        logging.info(f"Отправлен запрос на получение почты.")
        else:
            logging.info(f"Пользователь не найден в базе данных.")
        result = await handler(event, data)
        return result
