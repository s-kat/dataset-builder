from collections import defaultdict

import pytest
from app.main import add_key_value, double_word, quad


def test_one():
    a = 2
    assert quad(a) == 4

def test_two():
    a = 'ab'
    assert double_word(a) == a * 2

    d = add_key_value(defaultdict(int), 'b', 2)
    assert d == {'b': 2}
