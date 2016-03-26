
from __future__ import print_function

from collections import defaultdict
import itertools

from marker_helpers import ( get_direction_to_token_left,
                             get_direction_to_token_front,
                             get_direction_to_token_top,
                           )

from term import print_fail, print_ok, print_warn
from vectors import angle_between, are_same_direction

# Be very generous with the tolerance
import vectors
vectors.DEGREES_TOLERANCE = 35


class NetException(Exception):
    pass


# Via the itertools docs: https://docs.python.org/2/library/itertools.html#recipes
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


class TokenCheck(object):

    def __init__(self):
        self._all_angles = defaultdict(list)
        """Map of marker-pair to list of angles observed between that pair."""

        self.net = None
        """The net we're currently looking for.
           Initially empty, assigned when we first see a net."""


    @property
    def tokens_seen(self):
        return set(itertools.chain.from_iterable(self._all_angles.keys()))


    @property
    def complete(self):
        return len(self.tokens_seen) == 6


    @property
    def successful(self):
        assert self.complete, "Cannot reasonably determine success until check is complete"

        all_angles = itertools.chain.from_iterable(self._all_angles.values())

        return all(angle < vectors.DEGREES_TOLERANCE for angle in all_angles)


    def check_net(self, markers):
        assert markers, "No markers to get the nets of"

        nets = set()
        for m in markers:
            nets.add(m.info.token_net)

        if None in nets:
            raise NetException("Saw some non-token markers!")

        if self.net:
            extras = nets - set([self.net])
            if extras:
                others = ', '.join(extras)
                msg = "Saw markers from unexpected nets: {0} (expecting {1})."
                raise NetException(msg.format(others, self.net))

        else:
            if len(nets) != 1:
                raise NetException("Saw more than one net: {0}.".format(', '.join(nets)))

            self.net = nets.pop()


    def check_direction(self, name, func, markers):

        vectors = map(func, markers)
        all_same_direction = all(are_same_direction(*p) for p in pairwise(vectors))

        if not all_same_direction:
            print_fail("Token invalid -- {0} directions disagree!".format(name))

            for m in markers:
                print_fail('-', m.info.marker_type, m.info.code)
            for p in pairwise(vectors):
                print(angle_between(*p))

        return all_same_direction


    def check_directions(self, markers):
        assert len(markers) >= 2, "Not enough markers to check directions"

        left_dir_ok = self.check_direction('left', get_direction_to_token_left, markers)
        front_dir_ok = self.check_direction('front', get_direction_to_token_front, markers)
        top_dir_ok = self.check_direction('top', get_direction_to_token_top, markers)
        all_ok = left_dir_ok and front_dir_ok and top_dir_ok

        if all_ok:
            print_ok("View valid", end='')
            markers_str = ', '.join("{0} {1}".format(m.info.marker_type, m.info.code) \
                                    for m in markers)
            print(" (based on tokens: {0})".format(markers_str))

        return all_ok


    def process(self, markers):
        """Check that the given list of markers all belong to the same net and
           that they are positioned such that the net is correctly constructed.
        """

        if not markers:
            print_warn("No markers in sight")
            return

        self.check_net(markers)

        if len(markers) < 2:
            print_warn("Only one marker in sight")
            return

        self.check_directions(markers)
