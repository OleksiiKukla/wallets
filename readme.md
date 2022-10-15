# Wallets
___
Its single Rest app (Django). Implied than this service will be supplemented detached application (mobile or SPA).

## Description
___
- You can create wallets and provide transactions between them.
- Transactions are available only for wallets with the same currency(from USD to USD) 
- When user sends money from his wallet to his another wallet - no commission, and when he sends to wallet, related to another user - commission=10%
- User can register, login, logout
- User cant create more than 5 wallets
- You cant modify wallets data. PUT and PATCH are not available.
- When user created new wallet, he gets default bonus from bank. If wallet currency USD or EUR - balance=3.00. If RUB  - balance=100.00

## Getting Started
___
### Dependencies

- Python 3.9+

### Intall
___
~~~python
pip install django
pip install djangorestframework
pip install djoser
~~~
## How to use

- Create user (POST) <br/>
`registration/auth/users/`   - {
   "email": "email@email.com", 
   "username": "name", 
   "password": "password"
}
    


- Login (POST) <br/>
    `/login/login/` - {
   "username": "name", 
   "password": "password"
}



- Get auth_token (POST) <br/>
    `/auth/token/login` - {
   "email": "email@email.com", 
   "username": "name", 
   "password": "password"
}


- Create wallet (POST) <br/>
    `/wallets/` - {
    "type": "(visa or mastercard)",
    "currency": "(RUB, EUR, USD)"
}


- All users(current) wallets (GET) <br/>
    `/wallets/` 


- Wallet by name (GET) <br/>
    `/wallets/<name>`
  
  
- Delete wallet (DELETE) <br/>
    `/wallets/<name>`


- Create new transaction (POST) <br/>
    `/wallets/transactions/` - {
    "sender": "sender_wallet",
    "receiver": "receiver_wallet",
    "transfer_amount": "000.00"
}


- All transactions for current user (GET) <br/>
    `/wallets/transactions/` 


- Transaction by transaction ID (GET) <br/>
    `/wallets/transactions/<transaction_id>` 


- All transactions where wallet was sender or receiver (GET)<br/>
    `/wallets/transactions/<wallet_name>`
