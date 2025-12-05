from typing import List, Dict, Any


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество банковских операций по заданным категориям.
    Поиск осуществляется по полю 'description' в каждом словаре.

    Args:
        data: список словарей с данными об операциях. Каждый словарь должен содержать
                ключ 'description' с текстовым описанием операции.
        categories: список названий категорий для поиска.

    Returns:
        Словарь, где ключи — названия категорий, значения — количество операций,
        в которых описание содержит название категории (частичное совпадение).

    Пример:
        >>> data = [
        ...     {'id': 1, 'description': 'Покупка продуктов в магазине'},
        ...     {'id': 2, 'description': 'Оплата интернета'},
        ...     {'id': 3, 'description': 'Перевод другу'},
        ...     {'id': 4, 'description': 'Продукты и напитки'}
        ... ]
        >>> categories = ['продукты', 'интернет', 'перевод']
        >>> process_bank_operations(data, categories)
        {'продукты': 2, 'интернет': 1, 'перевод': 1}
    """
    # Инициализируем словарь результатов с нулевыми значениями
    result = {category: 0 for category in categories}

    for record in data:
        # Проверяем наличие поля description
        if "description" not in record:
            continue

        description = record["description"]
        # Приводим описание к строке и нижнему регистру для поиска
        if not isinstance(description, str):
            description = str(description)
        description_lower = description.lower()

        # Проверяем каждую категорию
        for category in categories:
            category_lower = category.lower()
            # Частичное совпадение: категория содержится в описании
            if category_lower in description_lower:
                result[category] += 1

    return result
