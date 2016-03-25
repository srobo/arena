
from collections import namedtuple
import math

WorldVector = namedtuple('WorldVector', ['x', 'y', 'z'])


def within_ten_percent(a, b):
    if a == b:
        return True

    if 0 in (a, b):
        return False

    frac = min(a, b) * 1.0 / max(a, b)
    return 0.9 <= frac


def unit_vector(direction_vector):
    size = math.sqrt(sum(x ** 2 for x in direction_vector))
    if size == 0:
        return direction_vector
    parts = [x / size for x in direction_vector]
    return WorldVector(*parts)


def are_same_direction(vec_a, vec_b):
    u_vec_a = unit_vector(vec_a)
    u_vec_b = unit_vector(vec_b)
    return all(map(within_ten_percent, u_vec_a, u_vec_b))


def make_vector(start, end):
    return WorldVector(end.x - start.x,
                       end.y - start.y,
                       end.z - start.z)
