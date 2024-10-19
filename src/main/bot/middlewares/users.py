from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, CallbackQuery
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.db.crud import users as user_crud
from src.main.utils.db_helper import db_helper


class AddUserMiddleware(BaseMiddleware):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> None:
        result = await handler(event, data)
        if event.message:
            user_id = event.message.from_user.id
            username = event.message.from_user.username
            chat_id = event.message.chat.id
            email = None
            state: FSMContext = data.get("state")
            if state:
                state_data = await state.get_data()
                email = state_data.get("email")
            if email:
                async with db_helper.session_factory() as session:
                    await user_crud.add_or_update_user(
                        session, user_id, username, email, chat_id
                    )
        return result
