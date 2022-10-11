from django.db import models


class Currensy_Choises(models.TextChoices):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"


class Type_Cards_Choises(models.TextChoices):
    visa = "visa"
    mastercard = "mastercard"
