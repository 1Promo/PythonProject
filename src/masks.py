def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.
    Формат маски: XXXX XX** **** XXXX
    Где X - это цифра номера карты
    """

    # Формируем маску
    masked_number = card_number[:4] + " " + card_number[4:6] + "** " + "**** " + card_number[-4:]

    return masked_number


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.
    Формат маски: XXXX XX** **** XXXX
    Где X - это цифра номера счета
    """

    # Формируем маску
    masked_account = "**" + account_number[-4:]

    return masked_account
