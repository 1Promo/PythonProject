import json
from pathlib import Path
from typing import List, Dict, Any


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список транзакций из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу с транзакциями

    Returns:
        Список словарей с данными о транзакциях. Если файл не найден, пустой или
        не содержит список, возвращает пустой список.

    """
    try:
        path = Path(file_path)
        if not path.exists() or path.stat().st_size == 0:
            return []

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []
