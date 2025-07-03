import random

from my_own.done.config import BAR_COUNT, RANGE


def generate_data(size=BAR_COUNT, min_val=RANGE[0], max_val=RANGE[1]):
    """Generates a list of random integers within a specified range."""
    return [random.randint(min_val, max_val) for _ in range(size)]


def generate_testing_data(size=40):
    return list(range(1, size + 1))