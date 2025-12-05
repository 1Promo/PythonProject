import re
from typing import List, Dict, Any


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет в списке словарей записи, где в поле 'description' (или аналогичном)
    содержится подстрока, соответствующая регулярному выражению search.

    Args:
        data: список словарей с данными об операциях. Ожидается, что каждый словарь
                содержит ключ 'description' (или настраиваемый) с текстовым описанием.
        search: строка поиска (регулярное выражение).

    Returns:
        Список словарей, где в описании найдено совпадение с шаблоном.

    Пример:
        >>> data = [
        ...     {'id': 1, 'description': 'Покупка в магазине продуктов'},
        ...     {'id': 2, 'description': 'Оплата интернета'},
        ...     {'id': 3, 'description': 'Перевод другу'}
        ... ]
        >>> process_bank_search(data, r'магазин')
        [{'id': 1, 'description': 'Покупка в магазине продуктов'}]
    """
    # Компилируем регулярное выражение для повышения производительности
    pattern = re.compile(search, re.IGNORECASE)  # Игнорируем регистр

    result = []
    for record in data:
        # Проверяем, есть ли ключ 'description' в словаре
        if "description" in record:
            description = record["description"]
            # Если значение не строковое, преобразуем в строку
            if not isinstance(description, str):
                description = str(description)
            # Проверяем соответствие регулярному выражению
            if pattern.search(description):
                result.append(record)

    return result
