
from __future__ import print_function

import itertools
import time

from sr.robot.vision import Vision, C500_focal_length

from marker_helpers import ( get_direction_to_token_left,
                             get_direction_to_token_front,
                             get_direction_to_token_top,
                             get_net )

from term import print_fail, print_ok, print_warn
from vectors import angle_between, are_same_direction

# Be very generous with the tolerance
import vectors
vectors.DEGREES_TOLERANCE = 30

RES = (1280,1024)


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

def process(markers):
    if not markers:
        print_warn("No markers in sight")
        return

    try:
        net = get_net(markers)
    except Exception as e:
        print_fail(e)
        return
    else:
        print_ok(net)

    if len(markers) < 2:
        print_warn("Only one marker in sight")
        return

    left_dir_ok = check_direction('left', get_direction_to_token_left, markers)
    front_dir_ok = check_direction('front', get_direction_to_token_front, markers)
    top_dir_ok = check_direction('top', get_direction_to_token_top, markers)

    if left_dir_ok and front_dir_ok and top_dir_ok:
        print_ok("Token valid")

#---

vis = Vision("/dev/video0", "../../../libkoki/lib", RES)
vis.camera_focal_length = C500_focal_length

def see():
    return vis.see('dev', 'A', RES, False)

while True:
    markers = see()

    print("I see", len(markers), "markers")

    process(markers)

    time.sleep(0.1)
