import logging
from logging_config import LoggerConfig

# Создаем логер для модуля utils
logger = LoggerConfig.create_logger("utils")


class UtilsModule:
    def process_data(self, data):
        try:
            logger.info("Начало обработки данных")

            if not isinstance(data, list):
                raise TypeError("Данные должны быть списком")

            # Имитация обработки данных
            processed_data = [x * 2 for x in data]
            logger.debug(f"Обработанные данные: {processed_data}")
            logger.info("Данные успешно обработаны")
            return processed_data

        except Exception as e:
            logger.error(f"Ошибка при обработке данных: {str(e)}")
            raise
