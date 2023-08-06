import itertools
import json
import pathlib


PATHFILE = pathlib.Path(__file__).absolute().parent

with open(PATHFILE / 'static/data.json', 'r') as f:
    data = json.load(f)

CONSONANT = data['consonant']
VOWEL = data['vowel']
REGULAR = data['tail']['regular']
IRREGULAR = data['tail']['irregular']
BREAK = data['tail']['break']


def syllable(s: str) -> list[str]:
    #! warning: do not alter this algorithm
    if 44032 <= (x := ord(s)) <= 55203:
        a = x - 44032
        b = a % 28
        c = 1 + ((a - b) % 588) // 28
        d = 1 + a // 588
        q = [*map(sum, zip(*[[d, c, b], [4351, 4448, 4519]]))]
        if b:
            return [*map(chr, q)]
        return [*map(chr, q[:2]), '']
    return ['', s, '']


def chunks(s: str) -> list[list, str]:
    a = [*itertools.chain(*map(syllable, s))]
    for i in range(r := len(a)):
        if i in range(1, r, 3):
            a[i] = list(a[i])
    a, b = ['', *a, ''], []
    for i in itertools.groupby(a, lambda e: isinstance(e, list)):
        b.append([*i[1]] if not i[0] else [*i[1]][0][0])
    return b


def word(s: str) -> str:
    r = ''
    for x in chunks(s):
        if isinstance(x, str):
            r += VOWEL[x] if x in VOWEL else x
        else:
            a, b = x
            if a:
                if b:
                    if a in IRREGULAR:
                        if ord(b) == 4363:
                            r += IRREGULAR[a][1]
                        else:
                            r += IRREGULAR[a][0]
                            r += CONSONANT[b]
                    else:
                        if '-'.join(x) in REGULAR:
                            r += REGULAR['-'.join(x)]
                        else:
                            r += BREAK[a]
                            r += CONSONANT[b]
                else:
                    r += BREAK[a]
            else:
                if b:
                    r += CONSONANT[b]
    return r


def romanize(s: str) -> str:
    r = ''
    for i in s.splitlines(True):
        r += ' '.join([*map(word, i.split(' '))])
    return r
