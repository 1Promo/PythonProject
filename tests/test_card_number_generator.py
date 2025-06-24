import unittest

from src.card_number_generator import card_number_generator


def card_number_format(param, param1):
    pass


class TestCardNumberGenerator(unittest.TestCase):

    def test_basic_range(self):
        # Проверяем базовый диапазон
        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005"
        ]
        result = list(card_number_generator(1, 5))
        self.assertEqual(result, expected)

    def test_single_value(self):
        # Проверяем генерацию одного значения
        expected = ["0000 0000 0000 1234"]
        result = list(card_number_generator(1234, 1234))
        self.assertEqual(result, expected)

    def test_large_numbers(self):
        # Проверяем работу с большими числами
        expected = [
            "9999 9999 9999 9998",
            "9999 9999 9999 9999"
        ]
        result = list(card_number_format(9999999999999998, 9999999999999999))
        self.assertEqual(result, expected)

    def test_formatting(self):
        # Проверяем корректность форматирования
        test_cases = [
            (1, "0000 0000 0000 0001"),
            (123, "0000 0000 0000 0123"),
            (123456, "0000 0001 2345 6000"),
            (123456789, "0012 3456 7890 0000"),
            (9999999999999999, "9999 9999 9999 9999")
        ]

        for number, expected in test_cases:
            result = next(card_number_generator(number, number))
            self.assertEqual(result, expected)

    def test_invalid_range(self):
        # Проверяем обработку некорректных диапазонов
        with self.assertRaises(ValueError):
            list(card_number_generator(10, 5))  # Начало больше конца

        with self.assertRaises(ValueError):
            list(card_number_generator(0, 5))  # Начало меньше допустимого

        with self.assertRaises(ValueError):
            list(card_number_generator(1, 10000000000000000))  # Конец больше допустимого

    def test_edge_cases(self):
        # Проверяем крайние значения диапазона
        result = list(card_number_generator(1, 1))
        self.assertEqual(result, ["0000 0000 0000 0001"])

        result = list(card_number_generator(9999999999999999, 9999999999999999))
        self.assertEqual(result, ["9999 9999 9999 9999"])

        result = list(card_number_generator(1000000000000000, 1000000000000000))
        self.assertEqual(result, ["1000 0000 0000 0000"])


if __name__ == '__main__':
    unittest.main()
