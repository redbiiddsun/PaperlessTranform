import random
import string


def generate_otp():
    return random.randint(100000, 999999)

def generate_otp_reference():
    number1 = str(random.randint(1, 9))
    number2 = str(random.randint(1, 9))
    char1 = random.choice(string.ascii_uppercase)
    char2 = random.choice(string.ascii_uppercase)
    char3 = random.choice(string.ascii_uppercase)

    return f"{number1}{char1}{number2}{char2}{char3}"