import random


def generate_sms_code() -> str:
    digits = range(10)
    return ''.join(map(str, random.sample(digits, 6)))
