import logging
import os
from logging.handlers import RotatingFileHandler

# Создаем директорию для логов, если её нет
if not os.path.exists("logs"):
    os.makedirs("logs")


class LoggerConfig:
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def create_logger(module_name):
        # Создаем логер
        logger = logging.getLogger(module_name)
        logger.setLevel(logging.DEBUG)  # Устанавливаем минимальный уровень логирования

        # Проверяем, чтобы избежать дублирования handlers
        if len(logger.handlers) > 0:
            return logger

        # Создаем обработчик для записи в файл
        file_handler = logging.FileHandler(f"logs/{module_name}.log", mode="w")
        file_handler.setLevel(logging.DEBUG)

        # Настраиваем формат вывода
        file_formatter = logging.Formatter(LoggerConfig.LOG_FORMAT, datefmt=LoggerConfig.DATE_FORMAT)
        file_handler.setFormatter(file_formatter)

        # Добавляем обработчик к логеру
        logger.addHandler(file_handler)

        return logger
