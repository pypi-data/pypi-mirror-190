import pytest
from word_tree import make_word_tree, next_char


@pytest.fixture()
def dictionary():
    return make_word_tree(['cat', 'dog', 'do', 'dot', 'pig', 'quit', 'deque'])


def test_next_char_word_no_next(dictionary):
    assert [None] == next_char(dictionary, 'dog')


def test_next_char_word_multiple_next(dictionary):
    assert ['g', 't', None] == next_char(dictionary, 'do')


def test_next_char_not_a_word(dictionary):
    assert [] == next_char(dictionary, 'date')


def test_qu_next(dictionary):
    assert ['q'] == next_char(dictionary, 'de')
