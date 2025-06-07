def filter_by_state(operations: list, state: str = 'EXECUTED') -> list:

    """Функция возвращает новый список словарей, содержащий только те словари, у которых ключ
state соответствует указанному значению."""

    filtered_list = []

    for operation in operations:
        if operation.get('state') == state:
            filtered_list.append(operation)

    return filtered_list


# Пример входных данных
data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

# Тестирование функции

# Случай 1: Фильтрация по умолчанию (EXECUTED)
executed_operations = filter_by_state(data)
print("Операции со статусом EXECUTED:")
print(executed_operations)


# Случай 2: Фильтрация по умолчанию CANCELED
canceled_operations = filter_by_state(data, 'CANCELED')
print("\nОперации со статусом CANCELED:")
print(canceled_operations)


"""Функция возвращает новый список, отсортированный по дате."""


def sort_by_date(operations: list, ascending: bool = False) -> list:
    return sorted(operations, key=lambda x: x['date'], reverse=not ascending)


# Список для сортировки операций
data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

# Сортировка по убыванию (по умолчанию)
print("\nСортировка по убыванию")
print(sort_by_date(data))
