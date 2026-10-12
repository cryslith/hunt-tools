#!/usr/bin/env python3

import argparse
from util import clean
from itertools import takewhile

# assumes words don't contain '$'
class RadixTree:
    def __init__(self, words):
        self.tree = {}
        for w in words:
            self.insert(w)

    def __locate(self, w):
        n = self.tree
        prev = None
        previ = None
        i = 0
        while True:
            if i >= len(w) or w[i] not in n:
                return previ, prev, i, n, None
            (branch, child) = n[w[i]]
            if not w[i:].startswith(branch):
                return previ, prev, i, n, w[i]
            previ = i
            prev = n
            i += len(branch)
            n = child

    def insert(self, w):
        w = w + '$'
        _, _, i, n, cont = self.__locate(w)
        if cont is None:
            if i >= len(w):
                # already present
                return
            n[w[i]] = (w[i:], {})
            return
        (branch, child) = n[cont]
        common = ''.join(x for x, _ in
                         takewhile((lambda z: z[0] == z[1]),
                                   zip(w[i:], branch)))
        n[cont] = (common, {
            w[i + len(common)]: (w[i + len(common):], {}),
            branch[len(common)]: (branch[len(common):], child)
        })

    def contains_prefix(self, w):
        _, _, i, n, cont = self.__locate(w)
        if cont is None:
            return i >= len(w)
        (branch, _) = n[cont]
        return branch.startswith(w[i:])

    def __contains__(self, w):
        return self.contains_prefix(w + '$')

    def delete(self, w):
        w = w + '$'
        raise NotImplementedError

# i wrote this radix tree implementation but building the radix tree is way slower than the search itself.
# so we don't actually use it.

def main():
    p = argparse.ArgumentParser(description='Solve word search')
    p.add_argument('file')
    p.add_argument('-w', '--word-list')
    args = p.parse_args()

    with open(args.word_list) as f:
        words = [clean(x) for x in f.readlines() if clean(x)]

    words = [x for x in words if len(x) >= 3]

    with open(args.file) as f:
        wordsearch = [[x.lower() for x in l.strip().split()] for l in f.readlines() if l.strip()]

    wordset = set(words)
    # wordtree = RadixTree(words)

    h = len(wordsearch)
    w = len(wordsearch[0])
    for i in range(h):
        for j in range(w):
            for d in [(0, 1), (0, -1), (1, 1), (-1, -1), (1, 0), (-1, 0), (1, -1), (-1, 1)]:
                z = []
                (y, x) = (i, j)
                while y >= 0 and y < h and x >= 0 and x < w:
                    z.append(wordsearch[y][x])
                    attempt = ''.join(z)
                    if attempt in wordset:
                        print(i, j, y, x, attempt)
                    # if attempt in wordtree:
                    #     print(i, j, y, x, attempt)
                    # elif not wordtree.contains_prefix(attempt):
                    #     break
                    y += d[0]
                    x += d[1]

if __name__ == '__main__':
    main()
