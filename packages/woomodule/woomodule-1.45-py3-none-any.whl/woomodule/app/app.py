from random import randint


def create_random_number():
    return str(randint(1, 10))


def get_number():
    result = create_random_number()
    print(f'From get_str func: {result}')
    return result