def transaction_descriptions(transactions):
    """
    Генератор для создания описаний транзакций

    Параметры:
    transactions (list) - список словарей с данными транзакций

    Каждый словарь должен содержать:
    - type (str) - тип транзакции (например, 'transfer', 'payment')
    - from_type (str) - тип отправителя ('card', 'account', 'organization')
    - to_type (str) - тип получателя ('card', 'account', 'organization')
    """
    for transaction in transactions:
        # Определяем базовое описание на основе типа транзакции
        if transaction['type'] == 'transfer':
            # Формируем описание для перевода
            if transaction['from_type'] == transaction['to_type']:
                if transaction['from_type'] == 'account':
                    yield "Перевод со счета на счет"
                elif transaction['from_type'] == 'card':
                    yield "Перевод с карты на карту"
            else:
                if transaction['from_type'] == 'organization':
                    yield "Перевод организации"
                elif transaction['to_type'] == 'organization':
                    yield "Перевод в организацию"
        elif transaction['type'] == 'payment':
            yield "Оплата услуги"
        else:
            yield "Неизвестная транзакция"


# Пример использования
transactions = [
    {'type': 'transfer', 'from_type': 'organization', 'to_type': 'account'},
    {'type': 'transfer', 'from_type': 'account', 'to_type': 'account'},
    {'type': 'transfer', 'from_type': 'account', 'to_type': 'account'},
    {'type': 'transfer', 'from_type': 'card', 'to_type': 'card'},
    {'type': 'transfer', 'from_type': 'organization', 'to_type': 'account'}
]

descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))
