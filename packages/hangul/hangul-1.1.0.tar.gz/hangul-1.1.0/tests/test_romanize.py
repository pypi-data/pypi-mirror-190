import hangul


def test_romanize():
    assert hangul.romanize('없을') == 'eopseul'

