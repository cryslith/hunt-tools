#!/usr/bin/env python3

import argparse
import collections
from itertools import *
from util import clean

def ngrams(s, n):
    return (s[i:i+n] for i in range(len(s)-n+1))

def main():
    p = argparse.ArgumentParser(description='Compute n-gram letter frequency.  Replaces all whitespace and non-ascii characters with single spaces.')
    p.add_argument('file')
    p.add_argument('n', type=int)
    p.add_argument('-s', '--no-spaces', action='store_true', help='remove spaces in input')
    args = p.parse_args()

    r = collections.defaultdict(lambda: 0)

    with open(args.file) as f:
        s = clean(f.read(), args.no_spaces)

    for w in ngrams(s, args.n):
        r[w] += 1

    result = list(r.items())
    result.sort(key=lambda x: x[1], reverse=True)
    for a, b in result:
        print(f'{a}: {b}')

if __name__ == '__main__':
    main()
