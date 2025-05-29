from my_own.done.config import BAR_COUNT, RANGE, CANVAS_WIDTH, CANVAS_HEIGHT

import random


def generate_data(size=BAR_COUNT, min_val=RANGE[0], max_val=RANGE[1]):
    """Generates a list of random integers within a specified range."""
    return [random.randint(min_val, max_val) for _ in range(size)]

