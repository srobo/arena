
from collections import namedtuple

WorldVector = namedtuple('WorldVector', ['x', 'y', 'z'])

def within_ten_percent(a, b):
    if a == b:
        return True

    if 0 in (a, b):
        return False

    frac = min(a, b) * 1.0 / max(a, b)
    return 0.9 <= frac

def are_same_direction(vec_a, vec_b):

    return all(map(within_ten_percent, vec_a, vec_b))
