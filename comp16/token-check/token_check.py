
from __future__ import print_function

from collections import defaultdict, Counter
import itertools

from marker_helpers import ( describe, describe_all,
                             get_direction_to_token_left,
                             get_direction_to_token_front,
                             get_direction_to_token_top,
                           )

from term import print_info, print_ok, print_warn
from vectors import angle_between, are_same_direction

# Be very generous with the tolerance
import vectors
vectors.DEGREES_TOLERANCE = 35


class NetException(Exception):
    pass


def median(numbers):
    items = list(sorted(numbers))
    count = len(items)
    if count % 2 == 0:
        l = items[count/2]
        r = items[(count+1)/2]
        return (l+r)/2.0
    else:
        return items[count/2]


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

    @property
    def likely_wrong_markers(self):
        """Determine which markers are likely wrongly placed by looking
           at their relative angles to other markers. We assume that
           all markers have the right net by this point.

           A correct token will have all markers' angles within tolerance.

           An incorrect token can feature:
           - completely correct markers, which border no invalid markers;
             these will have no wrong angles
           - correct markers which border an incorrect one; these will
             have a single pairing with an invalid angle
           - correct markers bordering several incorrect markers
           - incorrect markers
           These last two categories are potentially indistinguishable,
           since we don't collect data for all possible pairs -- we stop
           after having seen all the markers in at least one pair each.

           This property aims to return only markers in the last two categories
           and relies on the user handling the rest.
           This seems like a reasonable position since in all but simple
           cases, much of the token would need re-working and then re-checking
           anyway.
        """

        num_times_wrong = Counter()

        for pair, angles in self._all_angles.items():
            # Since we don't track which angles come from which directional
            # comparison, there's little benefit to comparing all of them
            if median(angles) >= vectors.DEGREES_TOLERANCE:
                num_times_wrong[pair[0]] += 1
                num_times_wrong[pair[1]] += 1

        likely_wrong = [code for code, count in num_times_wrong.items() if count > 1]

        return likely_wrong

    def check_net(self, markers):
        assert markers, "No markers to get the nets of"

        # Map: net -> list of markers with that net
        nets = defaultdict(list)
        for m in markers:
            nets[m.info.token_net].append(m)

        non_token_markers = nets.get(None)
        if non_token_markers:
            others = describe_all(non_token_markers)
            raise NetException("Saw some non-token markers: {0}!".format(others))

        if self.net:
            extras = set(nets.keys()) - set([self.net])
            if extras:
                msg = "Saw markers from unexpected nets (expecting {0}):".format(self.net)
                for n in extras:
                    msg += "\n {0}: {1}".format(n, describe_all(nets[n]))
                raise NetException(msg)

        else:
            if len(nets) != 1:
                raise NetException("Saw more than one net: {0}.".format(', '.join(nets)))

            self.net = nets.keys().pop()


    def check_direction(self, name, func, markers):

        # Map: code -> marker
        markers_map = {m.info.code: m for m in markers}

        # Map: code -> vector
        marker_vectors = {m.info.code: func(m) for m in markers}

        # List: all possible pairs of codes
        code_pairs = itertools.combinations(marker_vectors.keys(), 2)

        all_same_direction = True

        for pair in code_pairs:
            # normalise pair to ensure use as a dictionary key works as intended
            pair = pair if pair[0] <= pair[1] else (pair[1], pair[0])

            angle = angle_between(*[marker_vectors[code] for code in pair])

            self._all_angles[pair].append(angle)

            if angle >= vectors.DEGREES_TOLERANCE:
                all_same_direction = False
                print_warn("Token invalid -- {0} directions disagree ({1:.3f} degrees)!".format(name, angle))
                for code in pair:
                    kind = markers_map[code].info.marker_type
                    print_warn('-', kind, code)

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
            print_info("No markers in sight")
            return

        self.check_net(markers)

        if len(markers) < 2:
            print_info("Only one marker in sight")
            return

        self.check_directions(markers)
