import re
from string import ascii_lowercase

def clean(s, no_spaces=True):
    s = ('' if no_spaces else ' ').join(re.findall(r'[a-zA-Z]+', s))
    return s.lower()

A1 = {a: i+1 for i, a in enumerate(ascii_lowercase)}
A1R = {i: a for a, i in A1.items()}

def a1(s):
    return [A1[a] for a in s if a in A1]

def a1r(l, wrap=False):
    if wrap:
        return ''.join('z' if i%26 == 0 else A1R[i % 26] for i in l)
    return ''.join(A1R[i] for i in l)
