
from __future__ import print_function

BOLD = '\033[1m'
FAIL = '\033[91m'
OKBLUE = '\033[94m'
ENDC = '\033[0m'


def format_fail(*args):
    msg = ' '.join(map(str, args))
    return BOLD + FAIL + msg + ENDC

def print_fail(*args, **kargs):
    print(format_fail(*args), **kargs)


def format_ok(*args):
    msg = ' '.join(map(str, args))
    return BOLD + OKBLUE + msg + ENDC

def print_ok(*args, **kargs):
    print(format_ok(*args), **kargs)

