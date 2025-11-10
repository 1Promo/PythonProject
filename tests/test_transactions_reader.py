import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from io import StringIO
from transactions_reader import read_csv_transactions, read_excel_transactions

class TestTransactionsReader(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="дата,сумма,тип\n2023-01-01,1000,доход")
    @patch("pandas.read_csv")
    def test_read_csv_transactions_success(self, mock_open, mock_read_csv):
        # Настраиваем mock для pandas.read_csv
        mock_read_csv.return_value = pd.DataFrame({
            "дата": ["2023-01-01"],
            "сумма": [1000],
            "тип": ["доход"]
        })

        result = read_csv_transactions("dummy.csv")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["дата"], "2023-01-01")
        self.assertEqual(result[0]["сумма"], 1000)
        self.assertEqual(result[0]["тип"], "доход")

    @patch("os.path.exists")
    def test_read_csv_file_not_found(self, mock_exists):
        mock_exists.return_value = False

        with self.assertRaises(FileNotFoundError):
            read_csv_transactions("nonexistent.csv")

    @patch("pandas.read_csv")
    def test_read_csv_empty(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame()

        result = read_csv_transactions("empty.csv")
        self.assertEqual(result, [])

    @patch("os.path.exists")
    @patch("pandas.read_excel")
    def test_read_excel_transactions_success(self, mock_exists, mock_read_excel):
        mock_exists.return_value = True
        mock_read_excel.return_value = pd.DataFrame({
            "дата": ["2023-01-02"],
            "сумма": [500],
            "тип": ["расход"]
        })

        result = read_excel_transactions("dummy.xlsx")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["дата"], "2023-01-02")
        self.assertEqual(result[0]["сумма"], 500)
        self.assertEqual(result[0]["тип"], "расход")

    @patch("os.path.exists")
    def test_read_excel_file_not_found(self, mock_exists):
        mock_exists.return_value = False

        with self.assertRaises(FileNotFoundError):
            read_excel_transactions("nonexistent.xlsx")

    @patch("os.path.exists")
    @patch("pandas.read_excel")
    def test_read_excel_empty(self, mock_exists, mock_read_excel):
        mock_exists.return_value = True
        mock_read_excel.return_value = pd.DataFrame()

        result = read_excel_transactions("empty.xlsx")
        self.assertEqual(result, [])



if __name__ == "__main__":
    unittest.main()
