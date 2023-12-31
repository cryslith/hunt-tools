#!/usr/bin/env python3

import argparse
import re
import collections
import sys
from itertools import *

LETTER = r'[a-zA-Z]'

def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n-1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)

def count(l):
    for x in l:
        r[x] += 1
    return r

def text(filename, no_spaces=False):
    with open(filename) as f:
        s = f.read()
    s = ('' if no_spaces else ' ').join(re.findall(rf'{LETTER}+', s))
    s = s.lower()
    return s

def main():
    p = argparse.ArgumentParser(description='Compute n-gram letter frequency.  Replaces all whitespace and non-ascii characters with single spaces.')
    p.add_argument('file')
    p.add_argument('n', type=int)
    p.add_argument('-s', '--no-spaces', action='store_true', help='remove spaces in input')
    args = p.parse_args()

    r = collections.defaultdict(lambda: 0)

    s = text(args.file, args.no_spaces)
    for w in sliding_window(s, args.n):
        w = ''.join(w)
        r[w] += 1

    result = list(r.items())
    result.sort(key=lambda x: x[1], reverse=True)
    for a, b in result:
        print(f'{a}: {b}')

if __name__ == '__main__':
    main()
