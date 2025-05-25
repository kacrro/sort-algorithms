import random


def generate_data(size=20, min_val=1, max_val=100):
    return [random.randint(min_val, max_val) for _ in range(size)]
