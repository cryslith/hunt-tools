import re

LETTER = r'[a-zA-Z]'

def clean(s, no_spaces=True):
    s = ('' if no_spaces else ' ').join(re.findall(r'[a-zA-Z]+', s))
    return s.lower()
