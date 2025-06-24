def card_number_generator(start, end):
    # Проверяем корректность входных данных
    if not (1 <= start <= 9999999999999999):
        raise ValueError("Начальное значение должно быть от 1 до 9999999999999999")
    if not (1 <= end <= 9999999999999999):
        raise ValueError("Конечное значение должно быть от 1 до 9999999999999999")
    if start > end:
        raise ValueError("Начальное значение должно быть меньше или равно конечному")

    # Генерируем номера карт в заданном диапазоне
    for number in range(start, end + 1):
        # Форматируем число в строку с ведущими нулями
        formatted_number = f"{number:016d}"
        # Разбиваем на группы по 4 символа и добавляем пробелы
        card_number = (f"{formatted_number[0:4]} {formatted_number[4:8]}"
                       f"{formatted_number[8:12]} {formatted_number[12:16]}")
        yield card_number


# Пример использования
for card_number in card_number_generator(1, 5):
    print(card_number)

# Пример вывода:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
