import pytest
from src.processing import filter_by_state, sort_by_date

# Тестирование filter_by_state


def test_filter_by_state_existing():
    '''Проверяем фильтрацию при наличии подходящих элементов'''
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "PENDING"},
    ]
    result = filter_by_state(data, "EXECUTED")
    assert result == [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}]


@pytest.mark.parametrize("state", ["EXECUTED", "CANCELED", "PENDING"])
def test_filter_by_state_parametrized(state):
    '''Параметризованный тест для разных значений state'''
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "PENDING"},
    ]
    result = filter_by_state(data, state)
    assert all(item["state"] == state for item in result)


def test_filter_by_state_non_existing():
    '''Проверяем отсутствие элементов с указанным state'''
    data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}, {"id": 3, "state": "EXECUTED"}]
    result = filter_by_state(data, "PENDING")
    assert result == []


# Тестирование sort_by_date


def test_sort_by_date_desc():
    '''Проверка сортировки по убыванию date'''
    data = [{"id": 1, "date": "2023-01-01"}, {"id": 2, "date": "2023-03-01"}, {"id": 3, "date": "2023-02-01"}]
    result = sort_by_date(data)
    assert result == [
        {"id": 2, "date": "2023-03-01"},
        {"id": 3, "date": "2023-02-01"},
        {"id": 1, "date": "2023-01-01"},
    ]


def test_sort_by_date_asc():
    '''Проверка сортировки по возрастанию'''
    data = [{"id": 1, "date": "2023-01-01"}, {"id": 2, "date": "2023-03-01"}, {"id": 3, "date": "2023-02-01"}]
    result = sort_by_date(data, True)
    assert result == [
        {"id": 1, "date": "2023-01-01"},
        {"id": 3, "date": "2023-02-01"},
        {"id": 2, "date": "2023-03-01"},
    ]


def test_sort_by_date_same_dates():
    '''Проверка сортировки при одинаковых датах'''
    data = [{"id": 1, "date": "2023-01-01"}, {"id": 2, "date": "2023-01-01"}, {"id": 3, "date": "2023-01-01"}]
    result = sort_by_date(data)
    assert result == [
        {"id": 3, "date": "2023-01-01"},
        {"id": 2, "date": "2023-01-01"},
        {"id": 1, "date": "2023-01-01"},
    ]
