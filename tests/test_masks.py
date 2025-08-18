# Файл: tests/test_masks.py

import unittest
from src.masks import get_mask_card_number, get_mask_account


class TestMasks(unittest.TestCase):
    # Тесты для get_mask_card_number
    def test_card_number_masking(self):
        """
        Проверка корректного маскирования стандартных номеров карт
        """
        self.assertEqual(get_mask_card_number("4000111122223333"), "4000 11** **** 3333")
        self.assertEqual(get_mask_card_number("5123456789012345"), "5123 45** **** 2345")

    def test_card_number_edge_cases(self):
        """
        Проверка граничных случаев маскирования номеров карт
        """
        self.assertEqual(get_mask_card_number("400011112222333"), "4000 11** **** 2333")  # 15 цифр
        self.assertEqual(get_mask_card_number("40001111222233333"), "4000 11** **** 3333")  # 17 цифр

    def test_card_number_invalid_cases(self):
        """
        Проверка обработки некорректных номеров карт
        """
        self.assertEqual(get_mask_card_number(""), " ** **** ")  # Пустая строка
        self.assertEqual(get_mask_card_number("123"), "123 ** **** 123")  # Слишком короткий номер
        self.assertEqual(
            get_mask_card_number("123456789012345678901234567890"), "1234 56** **** 7890"
        )  # Слишком длинный номер
        self.assertEqual(get_mask_card_number("4000-1111-2222-3333"), "4000 -1** **** 3333")  # С дефисами

    # Тесты для get_mask_account
    def test_account_number_masking(self):
        """
        Проверка корректного маскирования стандартных номеров счетов
        """
        self.assertEqual(get_mask_account("40001111222233334444"), "**4444")
        self.assertEqual(get_mask_account("51234567890123456789"), "**6789")

    def test_account_number_edge_cases(self):
        """
        Проверка граничных случаев маскирования номеров счетов
        """
        self.assertEqual(get_mask_account("1234"), "**1234")  # 4 цифры
        self.assertEqual(get_mask_account("1234567890"), "**7890")  # 10 цифр

    def test_account_number_invalid_cases(self):
        """
        Проверка обработки некорректных номеров счетов
        """
        self.assertEqual(get_mask_account(""), "**")  # Пустая строка
        self.assertEqual(get_mask_account("12"), "**12")  # Слишком короткий номер
        self.assertEqual(get_mask_account("123456789012345678901234567890"), "**7890")  # Слишком длинный номер
        self.assertEqual(get_mask_account("4000-1111-2222-3333"), "**3333")  # С дефисами


if __name__ == "__main__":
    unittest.main()
