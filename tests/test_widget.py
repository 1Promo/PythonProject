# Файл: test_widget.py

import pytest
from src.widget import mask_account_card, get_date

# Тесты для mask_account_card


def test_card_masking() -> None:
    """
    Проверка корректности маскирования номеров карт различных типов
    """
    assert mask_account_card("Visa 4000111122223333") == "Visa 4000 11** **** 3333"
    assert mask_account_card("MasterCard 5123456789012345") == "MasterCard 5123 45** **** 2345"
    assert mask_account_card("Maestro 6000111122223333") == "Maestro 6000 11** **** 3333"
    assert mask_account_card("American Express 371449635398431") == "American Express 3714 49** **** 8431"


def test_account_masking() -> None:
    """
    Проверка корректности маскирования номеров счетов
    """
    assert mask_account_card("Счет 40001111222233334444") == "Счет **4444"
    assert mask_account_card("Счет 51234567890123456789") == "Счет **6789"
    assert mask_account_card("Счет 1234") == "Счет 1234"  # 4 цифры
    assert mask_account_card("Счет 1234567890") == "Счет **890"  # 10 цифр


@pytest.mark.parametrize(
    "input_data",
    [
        "",  # Пустая строка
        "Visa",  # Только тип без номера
        "1234567890",  # Только номер без типа
        "Visa 123",  # Некорректная длина номера
    ],
)
def test_invalid_input(input_data: str) -> None:
    """
    Проверка обработки некорректных входных данных
    """
    with pytest.raises(ValueError):
        mask_account_card(input_data)


# Тесты для get_date


def test_date_formatting() -> None:
    """
    Проверка корректности форматирования различных форматов даты
    """
    assert get_date("2025-06-14") == "14.06.2025"
    assert get_date("14.06.2025") == "14.06.2025"
    assert get_date("14/06/2025") == "14.06.2025"
    assert get_date("14 Jun 2025") == "14.06.2025"


def test_edge_cases() -> None:
    """
    Проверка граничных случаев форматирования дат
    """
    assert get_date("2025-01-01") == "01.01.2025"  # Первая дата года
    assert get_date("2025-12-31") == "31.12.2025"  # Последняя дата года
    assert get_date("2025-02-28") == "28.02.2025"  # Обычный февраль
    assert get_date("2024-02-29") == "29.02.2024"  # Високосный год


@pytest.mark.parametrize(
    "invalid_date",
    [
        "",  # Пустая строка
        "2025-13-32",  # Некорректный месяц и день
        "32.06.2025",  # Некорректный день
    ],
)
def test_invalid_dates(invalid_date: str) -> None:
    """
    Проверка обработки некорректных дат
    """
    with pytest.raises(ValueError):
        get_date(invalid_date)
