from aiogram import Dispatcher

# from src.main.bot.middlewares.courses import CourseMessageMiddleware


def setup(dp: Dispatcher):
    """
    Registers callback-query middleware
    :param dp: A `Dispatcher` instance
    """

    # dp.update.middleware(CourseMessageMiddleware())
