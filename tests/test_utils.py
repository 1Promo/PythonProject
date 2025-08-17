import json
import tempfile
from unittest.mock import patch, mock_open

from utils import load_transactions


def test_load_transactions_empty_file():
    with tempfile.NamedTemporaryFile() as tmp:
        assert load_transactions(tmp.name) == []


def test_load_transactions_not_list():
    data = {"key": "value"}
    with tempfile.NamedTemporaryFile(mode="w+") as tmp:
        json.dump(data, tmp)
        tmp.flush()
        assert load_transactions(tmp.name) == []


def test_load_transactions_valid_data():
    data = [{"id": 1}, {"id": 2}]
    with tempfile.NamedTemporaryFile(mode="w+") as tmp:
        json.dump(data, tmp)
        tmp.flush()
        assert load_transactions(tmp.name) == data


def test_load_transactions_file_not_found():
    assert load_transactions("nonexistent_file.json") == []


@patch("builtins.open", mock_open(read_data="invalid json"))
def test_load_transactions_invalid_json():
    assert load_transactions("any_path.json") == []
