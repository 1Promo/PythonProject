import pandas as pd
import os
from typing import List, Dict, Any


def read_csv_transactions(csv_path: str) -> List[Dict[str, Any]]:
    """
    Считывает транзакции из CSV-файла и возвращает список словарей.

    :param csv_path: путь к CSV-файлу
    :return: список словарей (каждая строка CSV → словарь)
    :raises FileNotFoundError: если файл не найден
    :raises ValueError: если ошибка при чтении
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV-файл не найден: {csv_path}")

    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        if df.empty:
            return []
        return df.to_dict(orient='records')
    except Exception as e:
        raise ValueError(f"Ошибка чтения CSV-файла: {e}")


def read_excel_transactions(xlsx_path: str) -> List[Dict[str, Any]]:
    """
    Считывает транзакции из Excel-файла и возвращает список словарей.

    :param xlsx_path: путь к Excel-файлу (.xlsx)
    :return: список словарей (каждая строка Excel → словарь)
    :raises FileNotFoundError: если файл не найден
    :raises ValueError: если ошибка при чтении
    """
    if not os.path.exists(xlsx_path):
        raise FileNotFoundError(f"Excel-файл не найден: {xlsx_path}")

    try:
        df = pd.read_excel(xlsx_path)
        if df.empty:
            return []
        return df.to_dict(orient='records')
    except Exception as e:
        raise ValueError(f"Ошибка чтения Excel-файла: {e}")
