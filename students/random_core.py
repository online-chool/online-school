import secrets
import string

def generate_random_digit_code(length=6):
    return ''.join(secrets.choice(string.digits) for _ in range(length))
