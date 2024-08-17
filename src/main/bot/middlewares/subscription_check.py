from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import TelegramObject, CallbackQuery

from src.config import settings


class SubscriptionCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> None:
        user = data["event_from_user"]
        bot: Bot = data["bot"]
        try:
            is_subscribed = await check_user_subscription(user.id, bot)
        except TelegramBadRequest as e:
            await event.message.answer(
                "Не удалось проверить вашу подписку. Пожалуйста, попробуйте еще раз."
            )
            print(f"Error checking subscription: {e}")  # For debugging purposes
            return await handler(event, data)
        if not is_subscribed:
            await event.message.answer(
                "Пожалуйста, подпишитесь на наш канал, чтобы продолжить."
            )
            return
        result = await handler(event, data)
        return result


async def check_user_subscription(user_id: int, bot: Bot) -> bool:
    try:
        # Ensure you're using the correct chat ID or username
        user_channel_status = await bot.get_chat_member(
            chat_id=settings.bot.channel_id, user_id=user_id
        )
        return user_channel_status.status != "left"
    except Exception as e:
        print(f"Error checking subscription: {e}")  # Add some logging for debugging
        return False
