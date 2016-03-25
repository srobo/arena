
from vectors import WorldVector, angle_between, are_same_direction, \
                    dot_product, unit_vector, within_ten_percent


def test_within_ten_percent():
    def check(a, b):
        assert within_ten_percent(a, b), \
                "{0} is within 10% of {1}".format(a, b)

    yield check, 0, 0
    yield check, 1, 1
    yield check, 1.1, 1
    yield check, 1.1, 1.1
    yield check, 1, 1.1
    yield check, 30, 31
    yield check, 90, 100

def test_not_within_ten_percent():
    def check(a, b):
        assert not within_ten_percent(a, b), \
                "{0} is not within 10% of {1}".format(a, b)

    yield check, -0.1, 0
    yield check, -0.1, 0.1
    yield check, -2, 1
    yield check, 1, 2
    yield check, 2, 1
    yield check, 1.5, 1
    yield check, 1.5, 1.1
    yield check, 1.1, 1.5
    yield check, 1, 1.5


def test_same_direction():
    def check(a, b):
        assert are_same_direction(a, b), \
                "{0} should be the same direction as {1}".format(a, b)

    yield check, WorldVector(1, 0, 1), WorldVector(1, 0, 1)
    yield check, WorldVector(1.1, 0, 1), WorldVector(1, 0, 1.1)
    yield check, WorldVector(2, 0, 2), WorldVector(1, 0, 1)

def test_not_same_direction():
    def check(a, b):
        assert not are_same_direction(a, b), \
                "{0} should not be the same direction as {1}".format(a, b)

    yield check, WorldVector(1, 0, 1), WorldVector(1, 1, 0)
    yield check, WorldVector(1, 0, 1), WorldVector(0, 0, 1)
    yield check, WorldVector(1, 0, 1), WorldVector(0, 0, 0)


def test_unit_vector():
    def check(vec, expected):
        unit_vec = unit_vector(vec)
        assert expected == unit_vec, \
                "Wrong unit vector for {0}.\n  Expected: {1}\n    Actual: {2}".format(vec, expected, unit_vec)

    yield check, WorldVector(1, 0, 0), WorldVector(1, 0, 0)
    yield check, WorldVector(2, 0, 0), WorldVector(1, 0, 0)


def test_dot_product_self():
    vec = WorldVector(1, 0, 0)
    dp = dot_product(vec, vec)
    assert dp == 1, "Dot product of a vector and itself is 1"

def test_dot_product_orthogonal():
    vec_a = WorldVector(1, 0, 0)
    vec_b = WorldVector(0, 1, 0)

    dp = dot_product(vec_a, vec_b)
    assert dp == 0, "Dot product of two perpendicular unit vectors is 0"

    dp = dot_product(vec_b, vec_a)
    assert dp == 0, "Dot product of two perpendicular unit vectors is 0"


def test_angle_between():
    def check(expected, vec_a, vec_b):
        actual = angle_between(vec_a, vec_b)
        assert expected == actual, \
                "Wrong angle between vectors.\n  Expected: {0}\n    Actual: {1}".format(expected, actual)

    yield check, 0, WorldVector(1, 0, 0), WorldVector(1, 0, 0)
    yield check, 180, WorldVector(1, 0, 0), WorldVector(-1, 0, 0)
    yield check, 90, WorldVector(1, 0, 0), WorldVector(0, 1, 0)
    yield check, 90, WorldVector(2, 0, 0), WorldVector(0, 0, 2)
