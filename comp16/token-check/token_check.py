
from __future__ import print_function

import itertools

from marker_helpers import ( get_direction_to_token_left,
                             get_direction_to_token_front,
                             get_direction_to_token_top,
                             get_net,
                             NetException )

from term import print_fail, print_ok, print_warn
from vectors import angle_between, are_same_direction

# Be very generous with the tolerance
import vectors
vectors.DEGREES_TOLERANCE = 30


# Via the itertools docs: https://docs.python.org/2/library/itertools.html#recipes
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def check_direction(name, func, markers):

    vectors = map(func, markers)
    all_same_direction = all(are_same_direction(*p) for p in pairwise(vectors))

    if not all_same_direction:
        print_fail("Token invalid -- {0} directions disagree!".format(name))
        for m in markers:
            print_fail('-', m.info.marker_type, m.info.code)
        for p in pairwise(vectors):
            print(angle_between(*p))

    return all_same_direction

def check_directions(markers):
    assert len(markers) >= 2, "Not enough markers to check directions"

    left_dir_ok = check_direction('left', get_direction_to_token_left, markers)
    front_dir_ok = check_direction('front', get_direction_to_token_front, markers)
    top_dir_ok = check_direction('top', get_direction_to_token_top, markers)
    all_ok = left_dir_ok and front_dir_ok and top_dir_ok

    if all_ok:
        print_ok("View valid", end='')
        markers_str = ', '.join("{0} {1}".format(m.info.marker_type, m.info.code) \
                                for m in markers)
        print(" (based on tokens: {0})".format(markers_str))

    return all_ok

def process(markers):
    """Check that the given list of markers all belong to the same net and
       that they are positioned such that the net is correctly constructed.

       Returns:
       - False: fail
       - None:  inconclusive (fewer than two markers in sight)
       - True:  valid
    """

    if not markers:
        print_warn("No markers in sight")
        return None

    try:
        net = get_net(markers)
    except NetException as ne:
        print_fail(ne)
        return False
    else:
        print_ok(net)

    if len(markers) < 2:
        print_warn("Only one marker in sight")
        return None

    return check_directions(markers)
