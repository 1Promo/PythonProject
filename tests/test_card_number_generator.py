from src.card_number_generator import card_number_generator


def test_card_number_format(random_card_number):
    assert len(random_card_number) == 19
    assert random_card_number.count(" ") == 3


def test_range_generation(card_number_range):
    start, end = card_number_range
    assert start < end
    assert 1 <= start <= 9999999999999999
    assert 1 <= end <= 9999999999999999
