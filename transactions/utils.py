from random import choice


from string import digits, ascii_uppercase


def create_name():
    random_name = digits + ascii_uppercase
    name = "".join(choice(random_name) for i in range(8))
    return name
