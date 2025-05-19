# Файл: src/widget.py

from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(info_string: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа
    строка с типом и номером (например, "Visa Platinum 7000792289606361")
    """
    # Разделяем строку на тип и номер
    parts = info_string.rsplit(" ", 1)

    # Проверяем, что строка содержит хотя бы два элемента
    if len(parts) < 2:
        return "Ошибка: некорректный формат данных"

    # Получаем тип и номер
    type_name = parts[0]
    number = parts[1]

    # Маскируем в зависимости от типа
    if type_name == "Счет":
        return f"{type_name} {get_mask_account(number)}"
    else:
        return f"{type_name} {get_mask_card_number(number)}"


# Примеры использования:
print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361
print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305
print(mask_account_card("Maestro 1596837868705199"))  # Maestro 1596 83** **** 5199
print(mask_account_card("MasterCard 7158300734726758"))  # MasterCard 7158 30** **** 6758
print(mask_account_card("Visa Classic 6831982476737658"))  # Visa Classic 6831 98** **** 7658
print(mask_account_card("Visa Gold 5999414228426353"))  # Visa Gold 5999 41** **** 6353
print(mask_account_card("Счет 35383033474447895560"))  # Счет **5560
print(mask_account_card("Счет 64686473678894779589"))  # Счет **9589


def get_date(date_string: str) -> str:
    # Разделяем исходную строку по символу 'T'
    date_part = date_string.split('T')[0]

    # Разделяем дату по символу '-'
    year, month, day = date_part.split('-')

    # Формируем итоговую строку в нужном формате
    result = f"{day}.{month}.{year}"

    return result


# Тестирование функции
input_date = "2024-03-11T02:26:18.671407"
formatted_date = get_date(input_date)
print(formatted_date)  # Вывод: 11.03.2024
