import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from typer import Typer, Option

from src.config import settings
from src.main.bot.app import get_dp

typer_app = Typer()


async def run_polling(dp: Dispatcher, bot: Bot) -> None:
    await dp.start_polling(bot)


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{settings.webhooks.host}{settings.webhooks.path}",
        secret_token=settings.webhooks.secret,
    )


@typer_app.command()
def start(
    use_webhook: bool = Option(
        default=False,
        help="Use webhook for receiving updates?",
    ),
):
    log_filename = "logs/course_bot.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename, encoding="UTF-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    dp = get_dp()
    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    if use_webhook:
        if settings.webhooks is None:
            print("Please, fill webhook's settings.")
            exit(-1)

        app = web.Application()
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=settings.webhooks.secret,
        )
        webhook_requests_handler.register(
            app,
            path=settings.webhooks.path,
        )
        setup_application(app, dp, bot=bot)
        web.run_app(
            app,
            host=settings.webserver.host,
            port=settings.webserver.port,
        )
    else:
        asyncio.run(run_polling(dp, bot))


if __name__ == "__main__":
    typer_app()
