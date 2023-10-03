from random import randint


def send_verify_code():
    code = randint(1000, 9999)
    print(code)
    return code
