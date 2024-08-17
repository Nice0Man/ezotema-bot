from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from . import handlers, middlewares


def get_dp() -> Dispatcher:
    """
    Initializes & returns `Dispatcher`
    """
    memory_storage = MemoryStorage()
    dp = Dispatcher(storage=memory_storage)
    handlers.setup(dp)
    middlewares.setup(dp)
    return dp
