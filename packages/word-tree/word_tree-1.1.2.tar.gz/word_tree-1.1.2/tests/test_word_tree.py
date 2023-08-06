import pytest
from word_tree import make_word_tree


@pytest.fixture()
def dictionary():
    return make_word_tree(['cat', 'dog', 'do', 'dot', 'pig', 'quit', 'deque'])


def test_next_char_word_no_next(dictionary):
    assert [None] == dictionary.next_char('dog')


def test_next_char_word_multiple_next(dictionary):
    assert ['g', 't', None] == dictionary.next_char('do')


def test_next_char_not_a_word(dictionary):
    assert [] == dictionary.next_char('date')


def test_qu_next(dictionary):
    assert ['q'] == dictionary.next_char('de')
