import time
import random
from functools import wraps


def exponential_backoff(max_retries=5, base_delay=1, max_delay=32):
    """
    Декоратор для реализации экспоненциального увеличения времени ожидания.

    :param max_retries: Максимальное количество попыток.
    :param base_delay: Базовое время ожидания в секундах.
    :param max_delay: Максимальное время ожидания в секундах.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    # Попытка выполнения обернутой функции
                    return func(*args, **kwargs)
                except Exception as e:
                    # Обработка ошибки
                    print(f"Ошибка: {e}")
                    # Вычисляем время ожидания
                    delay = min(max_delay, base_delay * (2**retries))
                    # Добавляем случайный разброс
                    delay = delay + random.uniform(0, 1)
                    print(f"Ожидание {delay:.2f} секунд перед повторной попыткой...")
                    time.sleep(delay)
                    retries += 1
            print("Превышено максимальное количество попыток.")
            return None

        return wrapper

    return decorator
