
from vectors import WorldVector, angle_between, are_same_direction, \
                    cross_product, dot_product, unit_vector, vector_sum

def test_same_direction():
    def check(a, b):
        assert are_same_direction(a, b), \
                "{0} should be the same direction as {1}".format(a, b)

    yield check, WorldVector(0.00001, 0, 1), WorldVector(-0.00001, 0, 1)
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


def test_vector_sum():
    def check(expected, *vectors):
        actual = vector_sum(*vectors)
        assert expected == actual, \
                "Wrong vector sum.\n  Expected: {0}\n    Actual: {1}".format(expected, actual)

    yield check, WorldVector(1, 0, 0), WorldVector(1, 0, 0), WorldVector(0, 0, 0)
    yield check, WorldVector(1, 1, 1), WorldVector(1, 0, 0), WorldVector(0, 1, 0), WorldVector(0, 0, 1)
    yield check, WorldVector(1, 1, 0), WorldVector(1, 0, -1), WorldVector(0, 1, 1)


def test_cross_product():
    def check(expected, vec_a, vec_b):
        cp = cross_product(vec_a, vec_b)
        assert expected == cp, \
                "Wrong cross product {0} x {1}.\n  Expected: {2}\n    Actual: {3}".format(vec_a, vec_b, expected, cp)

        # Also check the other way around, which is defined as the reverse
        expected_rev = WorldVector(*[-1 * x for x in expected])
        cp_rev = cross_product(vec_b, vec_a)
        assert expected_rev == cp_rev, \
                "Wrong cross product {0} x {1}.\n  Expected: {2}\n    Actual: {3}".format(vec_b, vec_a, expected_rev, cp_rev)

    # Self
    yield check, WorldVector(0, 0, 0), WorldVector(1, 0, 0), WorldVector(1, 0, 0)
    yield check, WorldVector(0, 0, 0), WorldVector(0, 1, 0), WorldVector(0, 1, 0)

    # Unit vectors
    yield check, WorldVector(1, 0, 0), WorldVector(0, 1, 0), WorldVector(0, 0, 1)
    yield check, WorldVector(0, -1, 0), WorldVector(1, 0, 0), WorldVector(0, 0, 1)

    # Other vectors
    yield check, WorldVector(4, 0, 0), WorldVector(0, 2, 0), WorldVector(0, 0, 2)


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
