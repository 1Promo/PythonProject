import csv
import json
from datetime import datetime
from typing import List, Dict, Any

import openpyxl

from services.bank_search import process_bank_search

from services.bank_operations import process_bank_operations


def load_json_data(filepath: str) -> List[Dict[str, Any]]:
    """Загружает данные из JSON‑файла."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка при чтении JSON‑файла: {e}")
        return []


def load_csv_data(filepath: str) -> List[Dict[str, Any]]:
    """Загружает данные из CSV‑файла."""
    try:
        data = []
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print(f"Ошибка при чтении CSV‑файла: {e}")
        return []


def load_xlsx_data(filepath: str) -> List[Dict[str, Any]]:
    """Загружает данные из XLSX‑файла."""
    try:
        wb = openpyxl.load_workbook(filepath)
        sheet = wb.active
        headers = [cell.value for cell in sheet[1]]
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append({headers[i]: row[i] for i in range(len(headers))})
        return data
    except Exception as e:
        print(f"Ошибка при чтении XLSX‑файла: {e}")
        return []


def filter_by_status(data: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу (регистронезависимо)."""
    return [
        item
        for item in data
        if "status" in item and isinstance(item["status"], str) and item["status"].strip().upper() == status.upper()
    ]


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате."""

    def parse_date(item):
        date_str = item.get("date", "")
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except (ValueError, TypeError):
            return datetime.min

    return sorted(data, key=parse_date, reverse=reverse)


def filter_ruble_transactions(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Оставляет только рублёвые транзакции."""
    return [
        item
        for item in data
        if "amount" in item and "currency" in item and item["currency"].strip().upper() in ["RUB", "РУБ"]
    ]


def format_transaction(item: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода."""
    date = item.get("date", "Неизвестно")
    description = item.get("description", "Нет описания")
    from_acc = item.get("from", "Не указан")
    to_acc = item.get("to", "Не указан")
    amount = item.get("amount", "Не указана")
    currency = item.get("currency", "Не указана")

    lines = [f"{date} {description}"]
    if from_acc:
        lines.append(f"{from_acc} -> {to_acc}")
    else:
        lines.append(f"Счет {to_acc}")
    lines.append(f"Сумма: {amount} {currency}")
    return "\n".join(lines)


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("> ").strip()

    data = []
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        filepath = input("Введите путь к JSON‑файлу: ").strip()
        data = load_json_data(filepath)
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        filepath = input("Введите путь к CSV‑файлу: ").strip()
        data = load_csv_data(filepath)
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        filepath = input("Введите путь к XLSX‑файлу: ").strip()
        data = load_xlsx_data(filepath)
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not data:
        print("Не удалось загрузить данные. Завершение программы.")
        return

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")
        status = input("> ").strip()
        if status.upper() in valid_statuses:
            break
        else:
            print(f'Статус операции "{status}" недоступен.')

    filtered_data = filter_by_status(data, status)
    print(f'Операции отфильтрованы по статусу "{status.upper()}"')

    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    sort_choice = input("Отсортировать операции по дате? Да/Нет\n> ").strip().lower()
    if sort_choice in ["да", "yes", "y"]:
        order = input("Отсортировать по возрастанию или по убыванию?\n> ").strip().lower()
        reverse = "убыванию" in order
        filtered_data = sort_by_date(filtered_data, reverse=reverse)

    # Фильтрация рублёвых транзакций
    ruble_choice = input("Выводить только рублевые транзакции? Да/Нет\n> ").strip().lower()
    if ruble_choice in ["да", "yes", "y"]:
        filtered_data = filter_ruble_transactions(filtered_data)

    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Поиск по слову в описании
    search_choice = (
        input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n> ").strip().lower()
    )
    if search_choice in ["да", "yes", "y"]:
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            filtered_data = process_bank_search(filtered_data, search_word)

    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Вывод результата
    print("Распечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(filtered_data)}\n")

    for i, item in enumerate(filtered_data, 1):
        print(format_transaction(item))
        if i < len(filtered_data):
            print()  # Пустая строка между транзакциями


if __name__ == "__main__":
    main()
