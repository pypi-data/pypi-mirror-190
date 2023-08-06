"""Utils"""
import random


def get_random_nums(min_num: int = 1, max_num: int = 45, cnt: int = 6):
    """Random numbers"""
    items = []
    while len(items) < cnt:
        tmp = str(random.randint(min_num, max_num))
        if tmp not in items:
            items.append(tmp)
    return items
