import functools
import logging
import traceback
from typing import Callable, Any


def log(filename: str = None) -> Callable:
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
                traceback.format_exc()
                logger.info(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise
            finally:
                for handler in logger.handlers:
                    handler.close()
                    logger.removeHandler(handler)

        return wrapper

    return decorator
