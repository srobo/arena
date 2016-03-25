
from vectors import cross_product, make_vector


def get_net(markers):
    assert markers, "No markers to get the nets of"

    nets = set()
    for m in markers:
        nets.add(m.info.token_net)

    assert None not in nets, "Saw some non-token markers!"

    assert len(nets) == 1, "Saw more than one net: {0}.".format(', '.join(nets))

    return nets.pop()


def get_direction_out_from_face(marker):
    """Returns the direction out from the marker towards the viewer,
       expressed as a ``WorldVector``."""

    to_top = get_direction_to_top(marker)
    to_right = get_direction_to_right(marker)

    return cross_product(to_top, to_right)


def get_direction_behind_face(marker):
    """Returns the direction away behind a marker,
       expressed as a ``WorldVector``."""

    to_top = get_direction_to_top(marker)
    to_right = get_direction_to_right(marker)

    return cross_product(to_right, to_top)


def get_direction_to_top(marker):
    """Returns the direction from the bottom to the top of the marker,
       expressed as a ``WorldVector``."""

    top_left, _, _, bottom_left = marker.vertices

    return make_vector(bottom_left.world, top_left.world)


def get_direction_to_right(marker):
    """Returns the direction from the left to the right of the marker,
       expressed as a ``WorldVector``."""

    top_left, top_right, _, _ = marker.vertices

    return make_vector(top_left.world, top_right.world)
