
from __future__ import print_function

from collections import namedtuple
import time

from sr.robot.vision import ( Vision, C500_focal_length,
                              MARKER_TOP, MARKER_BOTTOM, MARKER_SIDE,
                              NET_A, NET_B, NET_C )

BOLD = '\033[1m'
FAIL = '\033[91m'
OKBLUE = '\033[94m'
ENDC = '\033[0m'

RES = (1280,1024)

def format_fail(*args):
    msg = ' '.join(map(str, args))
    return BOLD + FAIL + msg + ENDC

def print_fail(*args, **kargs):
    print(format_fail(*args), **kargs)

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

    assert marker.maker_type == MARKER_SIDE, "Can't deal with top or bottom yet."

vis = Vision("/dev/video0", "../../../libkoki/lib", RES)
vis.camera_focal_length = C500_focal_length

def see():
    return vis.see('dev', 'A', RES, False)

while True:
    markers = see()

    print("I see", len(markers), "markers")

    for m in markers:
        #print(m.centre.polar, m.orientation)
        #print(m.centre.polar)
        print(m.info, m.orientation)

    net = None
    try:
        net = get_net(markers)
    except Exception as e:
        print_fail(e)
    else:
        print(OKBLUE + net + ENDC)

    assert net == NET_C





    time.sleep(0.1)
