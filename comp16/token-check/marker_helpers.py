
from sr.robot import ( MARKER_TOP, MARKER_BOTTOM, MARKER_SIDE,
                       NET_A, NET_B, NET_C )

from vectors import cross_product, make_vector


def get_net(markers):
    assert markers, "No markers to get the nets of"

    nets = set()
    for m in markers:
        nets.add(m.info.token_net)

    assert None not in nets, "Saw some non-token markers!"

    assert len(nets) == 1, "Saw more than one net: {0}.".format(', '.join(nets))

    return nets.pop()


def get_zone(marker):
    """Get the associated corner zone number for the marker."""

    assert marker.info.marker_type == MARKER_SIDE, \
            "Only token side markers have associated corner zones"

    FIRST_TOKEN_MARKER = 32

    # Use the fact that the markers are assigned in order to each token,
    # with the first two being top and bottom and the other four being
    # the zones (in ascending order); per the rules.
    zone = ((marker.info.code - FIRST_TOKEN_MARKER) % 6) - 2
    return zone


def is_left_side_token(marker):
    zone = get_zone(marker)
    net = marker.info.token_net
    return (net == NET_A and zone == 3) \
        or (net == NET_B and zone == 3) \
        or (net == NET_C and zone == 1)

def is_right_side_token(marker):
    zone = get_zone(marker)
    net = marker.info.token_net
    return (net == NET_A and zone == 1) \
        or (net == NET_B and zone == 2) \
        or (net == NET_C and zone == 2)

def is_rear_token(marker):
    zone = get_zone(marker)
    net = marker.info.token_net
    return (net == NET_A and zone == 2) \
        or (net == NET_B and zone == 1) \
        or (net == NET_C and zone == 3)


def get_direction_to_token_top(marker):
    """Return the direction to the top of the token, according to the
       given marker, expressed as a ``WorldVector``."""
    kind = marker.info.marker_type
    if kind == MARKER_SIDE:
        return get_direction_to_top(marker)

    elif kind == MARKER_TOP:
        return get_direction_out_from_face(marker)

    elif kind == MARKER_BOTTOM:
        return get_direction_behind_face(marker)

    else:
        assert False, "Unexpected marker type: {0}.".format(kind)


def get_direction_to_token_front(marker):
    """Return the direction to the front of the token, according to the
       given marker, expressed as a ``WorldVector``.
       The front of the token is the one which holds the side marker
       associated with corner 0.
    """
    kind = marker.info.marker_type
    if kind in (MARKER_TOP, MARKER_BOTTOM):
        return get_direction_to_top(marker)

    elif kind == MARKER_SIDE:
        zone = get_zone(marker)
        if zone == 0:
            return get_direction_out_from_face(marker)

        elif is_left_side_token(marker):
            return get_direction_to_left(marker)

        elif is_right_side_token(marker):
            return get_direction_to_right(marker)

        elif is_rear_token(marker):
            return get_direction_behind_face(marker)

        else:
            assert False, "Unexpected side marker: {0}.".format(marker.info)

    else:
        assert False, "Unexpected marker type: {0}.".format(kind)


def get_direction_to_token_left(marker):
    """Return the direction to the left of the token, according to the
       given marker, expressed as a ``WorldVector``.
       The left of the token is the one to the left when viewing an
       upright token from above.
    """
    kind = marker.info.marker_type
    if kind == MARKER_TOP:
        return get_direction_to_left(marker)

    elif kind == MARKER_BOTTOM:
        return get_direction_to_right(marker)

    elif kind == MARKER_SIDE:
        zone = get_zone(marker)
        if zone == 0:
            return get_direction_to_right(marker)

        elif is_left_side_token(marker):
            return get_direction_out_from_face(marker)

        elif is_right_side_token(marker):
            return get_direction_behind_face(marker)

        elif is_rear_token(marker):
            return get_direction_to_left(marker)

        else:
            assert False, "Unexpected side marker: {0}.".format(marker.info)

    else:
        assert False, "Unexpected marker type: {0}.".format(kind)


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


def get_direction_to_left(marker):
    """Returns the direction from the left to the right of the marker,
       expressed as a ``WorldVector``."""

    top_left, top_right, _, _ = marker.vertices

    return make_vector(top_right.world, top_left.world)


def get_direction_to_right(marker):
    """Returns the direction from the right to the right of the marker,
       expressed as a ``WorldVector``."""

    top_left, top_right, _, _ = marker.vertices

    return make_vector(top_left.world, top_right.world)
