from src.masks import mask_card_number, mask_account_number


def mask_account_card(data: str) -> str:
    """
    Функция маскирует номер карты или счёта в переданной строке.

    Примеры входных данных:
    - "Visa Platinum 7000792289606361"
    - "Maestro 7000792289606361"
    - "Счет 73654108430135874305"

    :param data: Строка с типом и номером карты или счёта
    :type data: str
    :return: Замаскированная строка в соответствии с видом (карта или счёт)
    :rtype: str

    Пример для карты:
    Вход: "Visa Platinum 7000792289606361"
    Выход: "Visa Platinum 7000 79** **** 6361"

    Пример для счёта:
    Вход: "Счет 73654108430135874305"
    Выход: "Счет **4305"
    """
    # Проверяем, является ли входным значением счёт
    if data.startswith("Счет"):
        # Разделяем строку на тип и номер
        splitted = data.split(maxsplit=1)
        # Маскируем номер счёта
        masked_number = mask_account_number(splitted[1])
        return f"{splitted[0]} {masked_number}"
    else:
        # Разделяем строку на тип и номер для карты
        splitted = data.rsplit(" ", 1)
        # Маскируем номер карты
        masked_number = mask_card_number(splitted[1])
        return f"{splitted[0]} {masked_number}"
