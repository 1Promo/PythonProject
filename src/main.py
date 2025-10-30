import pandas as pd


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


def read_transactions(file_path):
    """
    Считывает финансовые операции из файла (CSV или XLSX).

    Параметры:
        file_path (str): путь к файлу

    Возвращает:
        pd.DataFrame: данные транзакций
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, encoding='utf-8')
    elif file_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Поддерживаются только форматы CSV и XLSX")

    return df


# Использование
df: object = read_transactions('../data/transactions.csv')
# или
df = read_transactions('../data/transactions_excel.xlsx')

print(df.head())


def read_transactions(file_path, pd=None):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Поддерживаются только форматы CSV и XLSX")

        print(f"Успешно загружено {len(df)} строк.")
        return df

    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except pd.errors.EmptyDataError:
        print("Файл пуст.")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")

