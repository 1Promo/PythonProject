def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.
    Формат маски: XXXX XX** **** XXXX
    Где X - это цифра номера карты
    """

    # Формируем маску
    masked_number = card_number[:4] + " " + card_number[4:6] + "** " + "**** " + card_number[-4:]

    return masked_number


# Маскировка номера карты
print(get_mask_card_number("7000792289606361"))  # 7000 79** **** 6361
print(get_mask_card_number("4234567898765432"))  # 4234 56** **** 5432


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.
    Формат маски: XXXX XX** **** XXXX
    Где X - это цифра номера счета
    """

    # Формируем маску
    masked_account = "**" + account_number[:-17]

    return masked_account


# Маскировка номера счета
print(get_mask_account("407028107000000001233"))  # ****0000
print(get_mask_account("408028401000000005677"))  # ****0000
