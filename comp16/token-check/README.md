A utility for checking the tokens used in the SR2016 competition.

Needs:
- libkoki
- pykoki
- sr.robot, with at least I90f1ac030f7a145aaaa08e85d9d3e580849dbf44 and
  I3b0bd9141b8a34f38ac0d19a195310c7cf3463a6 applied.

Run tests with `nosetests`.

## Usage

Run the checker using `./check`

The token check program is designed to operate interactively, with a user
signalling the change-over from one token to the next.

When run it will output a stream of information about what markers it can
see, as well as what it is able to determine about the token as a result.

Once it has seen all 6 sides of the token it will emit a summary of whether
that token is correct or not. This information is based on the comparisons
made between pairs or triples of markers which were seen at any one time.

It should be noted that there are currently no checks that there is a chain
of comparisons which includes all markers, so it is theoretically possible
that a token could be wrong yet be found as being correct. This would require
that the system had only seen the token from completely isolated directions
and is believed to be unlikely.

After a given check is complete, the user is asked whether they wish to
check another token. This serves two purposes:
- it makes it clear to the user that the check is complete
- it allows the user to switch the token which is in the field of view
  without the system needing to guess that that is what is happening
  (as opposed to it seeing a poorly constructed token featuring markers
  from more than one token).
