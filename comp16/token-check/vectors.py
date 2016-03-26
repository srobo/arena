
from collections import namedtuple
import math

WorldVector = namedtuple('WorldVector', ['x', 'y', 'z'])

_ZERO_VECTOR = WorldVector(0, 0, 0)

# between vectors considered the same
DEGREES_TOLERANCE = 10


def cross_product(vec_a, vec_b):
    """Determines the cross product of the two vectors.
       Given vectors A and B, ``A x B == ||A|| ||B|| sin(theta)`` where
       theta is the angle between them.
    """

    return WorldVector( (vec_a.y * vec_b.z) - (vec_a.z * vec_b.y),
                        (vec_a.z * vec_b.x) - (vec_a.x * vec_b.z),
                        (vec_a.x * vec_b.y) - (vec_a.y * vec_b.x))


def dot_product(vec_a, vec_b):
    """Determines the dot product of the two vectors.
       Given vectors A and B, ``A . B == ||A|| ||B|| cos(theta)`` where
       theta is the angle between them.
    """
    dp = sum(a * b for a, b in zip(vec_a, vec_b))
    return dp


def angle_between(vec_a, vec_b):
    """Determine the angle between two vectors, in degrees.
       This is calculated using the definition of the dot product and
       knowing the size of the vectors.
    """

    dp = dot_product(vec_a, vec_b)
    mod_ab = vector_size(vec_a) * vector_size(vec_b)
    cos_theta = dp / mod_ab
    theta_rads = math.acos(cos_theta)
    theta_degrees = math.degrees(theta_rads)
    return theta_degrees


def vector_size(vec):
    size = math.sqrt(sum(x ** 2 for x in vec))
    return size


def vector_sum(*vectors):
    return WorldVector(*map(sum, zip(*vectors)))


def unit_vector(direction_vector):
    size = vector_size(direction_vector)
    if size == 0:
        return direction_vector
    parts = [x / size for x in direction_vector]
    return WorldVector(*parts)


def are_same_direction(vec_a, vec_b):
    if _ZERO_VECTOR in (vec_a, vec_b):
        return False

    theta = angle_between(vec_a, vec_b)
    return theta < DEGREES_TOLERANCE


def make_vector(start, end):
    return WorldVector(end.x - start.x,
                       end.y - start.y,
                       end.z - start.z)
