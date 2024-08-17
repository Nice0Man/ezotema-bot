from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiohttp import ClientSession

from src.config import settings


async def get_promo_code(city):
    async with ClientSession() as session:
        url = settings.api + "v1/promo-codes/generate"
        params = {"APP_ID": "2a4ff86f9aaa70041ec8e82db64abf56"}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()


class DiscountGenerationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> None:
        user_id = data["event_from_user"].id

        result = await handler(event, data)
        return result
