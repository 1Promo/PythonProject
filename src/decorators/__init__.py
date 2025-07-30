import functools
import logging
from typing import Callable, Any


def log(filename: str = None) -> Callable:
    """
    Декоратор для автоматического логирования выполнения функций.

    Параметры:
    filename (str, optional): Путь к файлу для записи логов.
        Если не указан, логи выводятся в консоль.

    Возвращает:
    Callable: Обёрнутую функцию с логированием.

    Декоратор автоматически логирует:
    - Начало и конец выполнения функции
    - Результат выполнения при успешном завершении
    - Информацию об ошибке и входные параметры при возникновении исключения

    Форматы логирования:
    - При успешном выполнении: "[имя_функции] ok"
    - При ошибке: "[имя_функции] error: [тип_ошибки]. Inputs: [аргументы]"

    Примеры использования:

    Базовый вариант (логирование в консоль):
    @log()
    def my_function(x, y):
        return x + y

    Вариант с указанием файла:
    @log(filename="mylog.txt")
    def my_function(x, y):
        return x + y

    Обработка ошибок:
    @log()
    def faulty_function(x):
        if x < 0:
            raise ValueError("Negative value")
        return x
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__name__)

            # Настройка логирования
            if filename:
                file_handler = logging.FileHandler(filename)
                logger.addHandler(file_handler)
            else:
                console_handler = logging.StreamHandler()
                logger.addHandler(console_handler)

            logger.setLevel(logging.INFO)
            formatter = logging.Formatter("%(message)s")
            for handler in logger.handlers:
                handler.setFormatter(formatter)

            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                logger.info(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise
            finally:
                for handler in logger.handlers:
                    handler.close()
                    logger.removeHandler(handler)

        return wrapper

    return decorator
