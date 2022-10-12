from random import choice


from string import digits, ascii_uppercase

# from transactions.models import Wallet            # спросить почему не работает


def create_name():
    """
    Create random name Wallet
    """
    random_name = digits + ascii_uppercase
    name = "".join(choice(random_name) for i in range(8))
    return name


def check_currency(sender_currency: str, receiver_currency: str):
    """
    Проверка на равенство валюты
    """
    if sender_currency != receiver_currency:
        return False
    return True


def check_balance(sender_balance: int, transer_amount: int):
    """
    Проверка на наличие денюжек на балансе
    """
    if transer_amount > sender_balance:
        return True
