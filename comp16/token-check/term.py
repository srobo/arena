
from __future__ import print_function

from functools import partial
import sys

BOLD = '\033[1m'
FAIL = '\033[91m'
WARN = '\033[38;5;130m'
OKBLUE = '\033[94m'
ENDC = '\033[0m'

if sys.version_info[0] == 3:
    raw_input = input


def _format(colour, *args):
    msg = ' '.join(map(str, args))
    return colour + msg + ENDC

def _print(formatter, *args, **kwargs):
    print(formatter(*args), **kwargs)


format_fail = partial(_format, BOLD + FAIL)
format_warn = partial(_format, BOLD + WARN)
format_ok = partial(_format, BOLD + OKBLUE)

print_fail = partial(_print, format_fail)
print_warn = partial(_print, format_warn)
print_ok = partial(_print, format_ok)


def query(question, yes_opts, no_opts):
    options = yes_opts + no_opts
    while True:
        answer = raw_input(question).lower()
        if answer not in options:
            print('Invalid input!')
        else:
            break

    return answer in yes_opts

def query_confirm(question):
    return query(question + " [Y/n]: ", ('y', ''), ('n',))
