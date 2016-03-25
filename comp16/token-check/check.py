
from __future__ import print_function

import itertools
import time

from sr.robot.vision import ( Vision, C500_focal_length,
                              MARKER_TOP, MARKER_BOTTOM, MARKER_SIDE,
                              NET_A, NET_B, NET_C )

from term import print_fail, print_ok
from vectors import make_vector, are_same_direction


RES = (1280,1024)


def get_net(markers):
    assert markers, "No markers to get the nets of"

    nets = set()
    for m in markers:
        nets.add(m.info.token_net)

    assert None not in nets, "Saw some non-token markers!"

    assert len(nets) == 1, "Saw more than one net: {0}.".format(', '.join(nets))

    return nets.pop()


def get_direction_to_top(marker):
    """Returns the direction from the bottom to the top of token as a
       ``WorldVector``, according to the given marker."""

    assert marker.info.marker_type == MARKER_SIDE, "Can't deal with top or bottom yet."

    top_left, _, _, bottom_left = marker.vertices

    return make_vector(bottom_left.world, top_left.world)


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

#print(list(pairwise('abc')))

while True:
    markers = see()

    print("I see", len(markers), "markers")

    for m in markers:
        #print(m.centre.polar, m.orientation)
        #print(m.centre.polar)
        print(m.info)
        #print(m.orientation)
        #print([v.image for v in m.vertices])
        print([v.world for v in m.vertices])

    try:
        net = get_net(markers)
        assert net == NET_C
    except Exception as e:
        print_fail(e)
    else:
        print_ok(net)

    if len(markers) > 1:
        # do processing to check the validity

        dirs_to_top = map(get_direction_to_top, markers)
        all_same_direction = all(are_same_direction(*p) for p in pairwise(dirs_to_top))
        print("all_same_direction:", all_same_direction)




    time.sleep(0.1)
