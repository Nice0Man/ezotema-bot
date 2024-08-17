from aiogram import Dispatcher


def setup(dp: Dispatcher):
    """
    Registers callback-query handlers
    :param dp: A `Dispatcher` instance
    """
    from .step_1 import router as step_1_router
    from .step_2 import router as step_2_router
    from .step_3 import router as step_3_router
    from .step_4 import router as step_4_router
    from .step_5 import router as step_5_router
    from .step_6 import router as step_6_router
    from .step_7 import router as step_7_router
    from .step_8 import router as step_8_router
    from .step_9 import router as step_9_router
    from .payment import router as payment_router

    dp.include_router(step_1_router)
    dp.include_router(step_2_router)
    dp.include_router(step_3_router)
    dp.include_router(step_4_router)
    dp.include_router(step_5_router)
    dp.include_router(step_6_router)
    dp.include_router(step_7_router)
    dp.include_router(step_8_router)
    dp.include_router(step_9_router)
    dp.include_router(payment_router)

    # from .test import router as test_router
    #
    # dp.include_router(test_router)
