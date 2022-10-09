from random import choice


from string import digits, ascii_uppercase

# from transactions.models import Wallet            # спросить почему не работает


def create_name():
    '''
    Create random name Wallet
    '''
    random_name = digits + ascii_uppercase
    name = "".join(choice(random_name) for i in range(8))
    return name

def check_currency(sender_currency: str, receiver_currency: str):
    '''
    Проверка на равенство валюты
    '''
    if sender_currency != receiver_currency:
            return False
    return True

def check_balance(sender_balance: int, transer_amount: int):
    '''
    Проверка на наличие денюжек на балансе
    '''
    if transer_amount > sender_balance:
        return True

def check_owner_wallet(seder_wallet, receiver_wallet):
    if seder_wallet == receiver_wallet:
        return True
#
# def check_receiver(sender: Wallet, receiver: Wallet):
#     '''
#     Проверка на наличие счета отправителя и получателя
#     ("Receiver does not exist ")
#     '''
#     try:
#         sender = Wallet.objects.get(id=sender)
#         receiver = Wallet.objects.get(id=receiver)
#     except ObjectDoesNotExist:
#         status = 'FAILED'
#         return

# def check_trancactions(sender: Wallet, receiver: Wallet):
#
#     elif check_balance(sender.balance < self.transer_amount):
#             self.status = 'FAILED - Not enough  money'
#         if sender.user is receiver.user:
#             self.commision = 0
#         else:
#             self.commision = self.transer_amount * 0.10
