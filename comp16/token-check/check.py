
from __future__ import print_function

import itertools
import time

from sr.robot.vision import ( Vision, C500_focal_length,
                              MARKER_TOP, MARKER_BOTTOM, MARKER_SIDE,
                              NET_A, NET_B, NET_C )

from marker_helpers import ( get_direction_behind_face,
                             get_direction_out_from_face,
                             get_direction_to_right,
                             get_direction_to_top,
                             get_net )

from term import print_fail, print_ok, print_warn
from vectors import make_vector, angle_between, are_same_direction

# Be very generous with the tolerance
import vectors
vectors.DEGREES_TOLERANCE = 30

RES = (1280,1024)


def get_direction_to_token_top(marker):
    kind = marker.info.marker_type
    if kind == MARKER_SIDE:
        return get_direction_to_top(marker)

    elif kind == MARKER_TOP:
        return get_direction_out_from_face(marker)

    elif kind == MARKER_BOTTOM:
        return get_direction_behind_face(marker)

    else:
        assert False, "Unexpected marker type: {0}.".format(kind)


# Via the itertools docs: https://docs.python.org/2/library/itertools.html#recipes
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

vis = Vision("/dev/video0", "../../../libkoki/lib", RES)
vis.camera_focal_length = C500_focal_length


def see():
    return vis.see('dev', 'A', RES, False)


def process(markers):
    if not markers:
        print_warn("No markers in sight")
        return

    try:
        net = get_net(markers)
    except Exception as e:
        print_fail(e)
    else:
        print_ok(net)

    if len(markers) < 2:
        print_warn("Only one marker in sight")
        return

    # do processing to check the validity

    dirs_to_top = map(get_direction_to_token_top, markers)
    all_same_direction = all(are_same_direction(*p) for p in pairwise(dirs_to_top))
    if all_same_direction:
        print_ok("Token valid")
    else:
        print_fail("Token invalid -- directions disagree!")
        for m in markers:
            print_fail('-', m.info.marker_type, m.info.code)
        for p in pairwise(dirs_to_top):
            print(angle_between(*p))

while True:
    markers = see()

    print("I see", len(markers), "markers")

    process(markers)

    time.sleep(0.1)
