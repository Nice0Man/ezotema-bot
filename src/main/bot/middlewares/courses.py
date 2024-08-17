from typing import Dict, Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.main.db.crud import course as course_crud
from src.main.utils.db_helper import db_helper


# class CourseMessageMiddleware(BaseMiddleware):
#     async def __call__(
#         self,
#         handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#         event: TelegramObject,
#         data: Dict[str, Any],
#     ) -> Any:
#         # Добавление курсов в данные для передачи обработчику
#         async with db_helper.session_factory() as session:
#             data["courses"] = await course_crud.get_all(session=session)
#         result = await handler(event, data)
#         await db_helper.dispose()
#         return result
