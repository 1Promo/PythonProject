# conftest.py
import pytest
import random
from datetime import datetime

# Фикстура для генерации случайного номера карты
@pytest.fixture
def random_card_number():
    """
    Генерирует случайный валидный номер карты в формате XXXX XXXX XXXX XXXX
    """
    number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
    formatted = f"{number[0:4]} {number[4:8]} {number[8:12]} {number[12:16]}"
    return formatted

# Фикстура для генерации диапазона номеров карт
@pytest.fixture
def card_number_range():
    """
    Возвращает кортеж с начальным и конечным номером для тестирования диапазона
    """
    start = random.randint(1, 9999999999999990)
    end = start + random.randint(1, 100)
    return (start, end)

# Фикстура для генерации тестовых данных с разными форматами
@pytest.fixture(params=[
    (1, "0000 0000 0000 0001"),
    (123456789, "0012 3456 7890 0000"),
    (9999999999999999, "9999 9999 9999 9999"),
    (5000000000000000, "5000 0000 0000 0000")
])
def test_format_data(request):
    """
    Параметризованная фикстура для тестирования форматирования
    """
    return request.param

# Фикстура для генерации некорректных входных данных
@pytest.fixture(params=[
    (0, "Значение меньше допустимого"),
    (10000000000000000, "Значение больше допустимого"),
    (10, 5, "Обратный диапазон"),
])
def invalid_input_data(request):
    """
    Данные для тестирования обработки ошибок
    """
    return request.param

# Фикстура для генерации временных меток
@pytest.fixture
def timestamp():
    """
    Возвращает текущую временную метку
    """
    return int(datetime.now().timestamp())

import pytest
from typing import List, Dict

# Фикстура для создания пустого списка транзакций
@pytest.fixture
def empty_transactions() -> List[Dict[str, str]]:
    """
    Возвращает пустой список транзакций
    """
    return []

# Фикстура для создания базового набора транзакций
@pytest.fixture
def basic_transactions() -> List[Dict[str, str]]:
    """
    Возвращает список с базовыми типами транзакций
    """
    return [
        {'type': 'transfer', 'from_type': 'organization', 'to_type': 'account'},
        {'type': 'transfer', 'from_type': 'account', 'to_type': 'account'},
        {'type': 'transfer', 'from_type': 'card', 'to_type': 'card'},
        {'type': 'payment', 'from_type': 'account', 'to_type': 'service'}
    ]

# Фикстура для создания транзакций с разными комбинациями
@pytest.fixture
def mixed_transactions() -> List[Dict[str, str]]:
    """
    Возвращает список с разными комбинациями отправителя и получателя
    """
    return [
        {'type': 'transfer', 'from_type': 'organization', 'to_type': 'card'},
        {'type': 'transfer', 'from_type': 'card', 'to_type': 'organization'},
        {'type': 'transfer', 'from_type': 'account', 'to_type': 'card'},
        {'type': 'transfer', 'from_type': 'card', 'to_type': 'account'}
    ]

# Фикстура для создания транзакций с неизвестным типом
@pytest.fixture
def unknown_type_transactions() -> List[Dict[str, str]]:
    """
    Возвращает список с транзакциями неизвестного типа
    """
    return [
        {'type': 'unknown', 'from_type': 'account', 'to_type': 'account'}
    ]

# Функция для фильтрации транзакций по валюте
def filter_by_currency(transactions, currency_code):
    for tx in transactions:
        try:
            if tx['operationAmount']['currency']['code'] == currency_code:
                yield tx
        except KeyError:
            continue

# Функция для получения описаний транзакций
def transaction_descriptions(transactions):
    for tx in transactions:
        try:
            yield tx['description']
        except KeyError:
            continue

# Фикстуры с тестовыми данными
def create_usd_transactions():
    return [
        {
            "id": 939719570,
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод организации"
        },
        {
            "id": 142264268,
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод со счета на счет"
        }
    ]

def create_rub_transactions():
    return [
        {
            "id": 873106923,
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод со счета на счет"
        }
    ]

def create_mixed_transactions():
    return create_usd_transactions() + create_rub_transactions()

def create_invalid_transactions():
    return [
        {
            "id": 123,
            "operationAmount": "invalid_data",
            "description": "Невалидная транзакция"
        },
        {
            "id": 456,
            "operationAmount": {
                "amount": "100",
                "currency": {"name": "EUR", "code": "EUR"}
            }
        }
    ]
# Функции для работы с транзакциями
def filter_by_currency(transactions, currency):
    for tx in transactions:
        if tx.get('operationAmount', {}).get('currency', {}).get('code') == currency:
            yield tx

def get_descriptions(transactions):
    for tx in transactions:
        yield tx.get('description', '')

# Фикстуры с тестовыми данными
def usd_transactions():
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "100", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод 1"
        },
        {
            "id": 2,
            "operationAmount": {"amount": "200", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод 2"
        }
    ]

def rub_transactions():
    return [
        {
            "id": 3,
            "operationAmount": {"amount": "300", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод 3"
        }
    ]

def mixed_transactions():
    return usd_transactions() + rub_transactions()

def invalid_transactions():
    return [
        {"id": 4, "description": "Без валюты"},
        {"id": 5, "operationAmount": "невалидные данные"}
    ]

# Функции для работы с транзакциями
def filter_by_currency(transactions, currency):
    for tx in transactions:
        if tx.get('operationAmount', {}).get('currency', {}).get('code') == currency:
            yield tx

def get_descriptions(transactions):
    for tx in transactions:
        yield tx.get('description', '')

# Фикстуры с тестовыми данными
def usd_transactions():
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "100", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод 1"
        },
        {
            "id": 2,
            "operationAmount": {"amount": "200", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод 2"
        }
    ]

def rub_transactions():
    return [
        {
            "id": 3,
            "operationAmount": {"amount": "300", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод 3"
        }
    ]

def mixed_transactions():
    return usd_transactions() + rub_transactions()

def invalid_transactions():
    return {
        {"id": 4, "description": "Без валюты"},
        {"id": 5, "operationAmount": "невалидные данные"}
    }