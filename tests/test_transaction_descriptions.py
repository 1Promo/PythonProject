from src.transaction_descriptions import transaction_descriptions


def test_transaction_descriptions():
    # Тест 1: Базовый случай с разными типами транзакций
    transactions1 = [
        {'type': 'transfer', 'from_type': 'organization', 'to_type': 'account'},
        {'type': 'transfer', 'from_type': 'account', 'to_type': 'account'},
        {'type': 'transfer', 'from_type': 'card', 'to_type': 'card'},
        {'type': 'payment', 'from_type': 'account', 'to_type': 'service'}
    ]
    expected1 = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Оплата услуги"
    ]

    descriptions1 = transaction_descriptions(transactions1)
    assert list(descriptions1) == expected1

    # Тест 2: Пустой список транзакций
    transactions2 = []
    expected2 = []

    descriptions2 = transaction_descriptions(transactions2)
    assert list(descriptions2) == expected2

    # Тест 3: Одна транзакция
    transactions3 = [
        {'type': 'transfer', 'from_type': 'organization', 'to_type': 'organization'}
    ]
    expected3 = ["Перевод организации"]

    descriptions3 = transaction_descriptions(transactions3)
    assert list(descriptions3) == expected3

    # Тест 4: Транзакции с разными комбинациями отправителя и получателя
    transactions4 = [
        {'type': 'transfer', 'from_type': 'organization', 'to_type': 'card'},
        {'type': 'transfer', 'from_type': 'card', 'to_type': 'organization'},
        {'type': 'transfer', 'from_type': 'account', 'to_type': 'card'},
        {'type': 'transfer', 'from_type': 'card', 'to_type': 'account'}
    ]
    expected4 = [
        "Перевод организации",
        "Перевод организации",
        "Перевод со счета на счет",  # Предполагается, что card считается как account
        "Перевод со счета на счет"
    ]

    descriptions4 = transaction_descriptions(transactions4)
    assert list(descriptions4) == expected4

    # Тест 5: Неизвестный тип транзакции
    transactions5 = [
        {'type': 'unknown', 'from_type': 'account', 'to_type': 'account'}
    ]
    expected5 = ["Неизвестная транзакция"]

    descriptions5 = transaction_descriptions(transactions5)
    assert list(descriptions5) == expected5

    print("Все тесты пройдены!")


# Запуск тестов
test_transaction_descriptions()
