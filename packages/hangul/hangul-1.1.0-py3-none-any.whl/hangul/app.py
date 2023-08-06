import functools
import itertools
import json
import os


class __hangul__:
    
    def __init__(self, text: str):
        self.text = text
    
    def syllable(self, s: str) -> list[str]:
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
    
    def chunk(self, s: str) -> list[list, str]:
        a = [*itertools.chain(*map(self.syllable, s))]
        for i in range(r := len(a)):
            if i in range(1, r, 3):
                a[i] = list(a[i])
        a, b = ['', *a, ''], []
        for i in itertools.groupby(a, lambda e: isinstance(e, list)):
            b.append([*i[1]] if not i[0] else [*i[1]][0][0])
        return b
    
    def word(self, s: str) -> str:
        r = ''
        for x in self.chunk(s):
            if isinstance(x, str):
                r += self.vowel[x] if x in self.vowel else x
            else:
                a, b = x
                if a:
                    if b:
                        if a in self.blend:
                            if ord(b) == 4363:
                                r += self.blend[a][1]
                            else:
                                r += self.blend[a][0]
                                r += self.consonant[b]
                        else:
                            if '-'.join(x) in self.special:
                                r += self.special['-'.join(x)]
                            else:
                                r += self.period[a]
                                r += self.consonant[b]
                    else:
                        r += self.period[a]
                else:
                    if b:
                        r += self.consonant[b]
        return r
    
    def __str__(self) -> str:
        r = ''
        for i in self.text.splitlines(True):
            r += ' '.join([*map(self.word, i.split(' '))])
        return r
    
    @property
    @functools.cache
    def data(self):
        path = os.path.dirname(__file__)
        with open(f'{path}/static/data.json', 'r') as f:
            return json.load(f)
    
    @property
    def consonant(self):
        return self.data['consonant']
    
    @property
    def vowel(self):
        return self.data['vowel']
    
    @property
    def special(self):
        return self.data['tail']['special']
    
    @property
    def blend(self):
        return self.data['tail']['blend']
    
    @property
    def period(self):
        return self.data['tail']['period']


def romanize(text: str) -> str:
    if isinstance(text, str):
        return __hangul__(text).__str__()
    else:
        raise TypeError('The `text` argument must be a string.')
