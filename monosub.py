#!/usr/bin/env python3

import argparse
import math
import random
import string
from util import clean

single_order = 'etaoinshrdlcumwfgypbvkjxqz'
NEGATIVE_INFINITY = -20
ITERATIONS = 10000

def ngrams(s, n):
    return (s[i:i+n] for i in range(len(s)-n+1))

def read_frequencies(filename):
    r = {}
    with open(filename) as f:
        for l in f:
            l = l.strip('\n')
            if not l:
                continue
            a, b = l.split(': ')
            r[a] = int(b)
    return r

def logprobs(ngrams):
    n = sum(ngrams.values())
    r = {}
    for q, v in ngrams.items():
        r[q] = math.log(v / n)
    return r

def decrypt(s, key):
    table = str.maketrans(single_order, key)
    return(s.translate(table))

def fitness(ngram_size, lpq, s, key):
    t = decrypt(s, key)
    return sum(lpq[w] if w in lpq else NEGATIVE_INFINITY
               for w in ngrams(t, ngram_size)) / (len(t) - ngram_size + 1)

def random_neighbor(key):
    # generate a random neighbor of the key by swapping two random letters
    key = list(key)
    i = random.randrange(1, len(key))
    j = random.randrange(0, i)
    key[i], key[j] = key[j], key[i]
    yield ''.join(key)

def neighbors(key):
    # generate all neighbors of the key by swapping two letters
    key = list(key)
    for i in range(1, len(key)):
        for j in range(i):
            key[i], key[j] = key[j], key[i]
            yield ''.join(key)
            key[i], key[j] = key[j], key[i]

def random_key():
    key = list(single_order)
    random.shuffle(key)
    return ''.join(key)

def search(ngram_size, lpq, s, use_random_neighbor=False):
    # a key is a permutation of letters, represented by a permutation of single-letter frequency order
    key = random_key() 
    cf = fitness(ngram_size, lpq, s, key)
    i = 0
    for i in range(ITERATIONS):
        print(cf, decrypt(s, key))
        ns = random_neighbor(key) if use_random_neighbor else neighbors(key)
        ns = ((fitness(ngram_size, lpq, s, newkey), newkey)
              for newkey in ns)
        nf, newkey = max(ns)
        if nf > cf:
            key, cf = newkey, nf
        elif not use_random_neighbor:
            return key
        i += 1
    return key

def main():
    p = argparse.ArgumentParser(description='Break monoalphabetic substitution cipher using hill climbing.')
    p.add_argument('file')
    p.add_argument('-n', '--ngram-size', type=int, default=3)
    p.add_argument('-f', '--frequencies', help='ngram frequency table')
    p.add_argument('-s', '--no-spaces', action='store_true', help='remove spaces in input')
    p.add_argument('-e', '--encrypt', action='store_true', help='randomly encrypt input instead of breaking')
    args = p.parse_args()

    with open(args.file) as f:
        s = clean(f.read(), args.no_spaces)

    if args.encrypt:
        print(decrypt(s, random_key()))
        return

    ng = args.frequencies
    if ng is None:
        ng = f'frequencies/without_spaces_{args.ngram_size}' if args.no_spaces else f'frequencies/with_spaces_{args.ngram_size}'
    ng = read_frequencies(ng)
    lpq = logprobs(ng)

    key = search(args.ngram_size, lpq, s, True)
    print(decrypt(s, key))


if __name__ == '__main__':
    main()
