def clear_names(file_name: str) -> list:
    """Функция для очистки имен от лишних символов"""
    new_names_list = list()
    with open("data/" + file_name) as names_file:
        names_list = names_file.read().split()
        for name_item in names_list:
            new_name = ""
            for symbol in name_item:
                if symbol.isalpha():
                    new_name += symbol
            if new_name.isalpha():
                new_names_list.append(new_name)
    return new_names_list


if __name__ == "__main__":
    cleared_name = clear_names("../data/names.txt")

    for i in cleared_name:
        print(i)

from transactions_reader import read_csv_transactions, read_excel_transactions


# Пути к файлам
csv_path = "../data/transactions.csv"
xlsx_path = "../data/transactions.xlsx"


# Чтение CSV
try:
    csv_data = read_csv_transactions(csv_path)
    print(f"CSV: {len(csv_data)} транзакций")
    for t in csv_data[:2]:  # первые 2 транзакции
        print(t)
except Exception as e:
    print(f"Ошибка CSV: {e}")


# Чтение Excel
try:
    excel_data = read_excel_transactions(xlsx_path)
    print(f"\nExcel: {len(excel_data)} транзакций")
    for t in excel_data[:2]:  # первые 2 транзакции
        print(t)
except Exception as e:
    print(f"Ошибка Excel: {e}")
