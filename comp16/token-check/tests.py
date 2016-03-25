
from vectors import WorldVector, are_same_direction, unit_vector, within_ten_percent


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
