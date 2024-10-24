"""
test_linkedlist.py

This file contains the tests for the LinkedList class.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""


import pytest

from LinkedList import *
import numpy as np

@pytest.fixture
def empty_ll():
    return LinkedList()

@pytest.fixture
def sample_ll():
    # 3 2 1
    ll = LinkedList()
    ll.insert_last(3)
    ll.insert_last(2)
    ll.insert_last(1)
    return ll

def test_insert_first(empty_ll):
    empty_ll.insert_first(150)
    empty_ll.insert_first(350)
    assert 350 == empty_ll[0].get_value()
    assert 150 == empty_ll[1].get_value()

def test_insert_last(empty_ll):
    empty_ll.insert_last(150)
    empty_ll.insert_last(350)
    assert 150 == empty_ll[0].get_value()
    assert 350 == empty_ll[1].get_value()

def test_insert_before(sample_ll):
    sample_ll.insert_before(2.5, 2)
    assert len(sample_ll) == 4
    assert 2.5 == sample_ll[2].get_value()

def test_remove(sample_ll):
    assert len(sample_ll) == 3

    sample_ll.remove_first()
    assert 2 == sample_ll[0].get_value()
    assert 1 == sample_ll[1].get_value()
    assert len(sample_ll) == 2

    sample_ll.remove_last()
    assert 2 == sample_ll[0].get_value()
    with pytest.raises(IndexError):
        assert not sample_ll[1]
    assert len(sample_ll) == 1

    sample_ll.remove_at(0)
    assert len(sample_ll) == 0
    with pytest.raises(IndexError):
        assert not sample_ll[0]

def test_remove_empty(empty_ll):
    with pytest.raises(ListEmpty):
        empty_ll.remove_first()

def test_print_list(sample_ll, capsys):
    sample_ll.print_list()
    captured = capsys.readouterr()
    assert captured.out == "[1] 3 -> [2] 2 -> [3] 1\n"

def test_iterator(sample_ll):
    result = np.empty(len(sample_ll), dtype=int)
    expected = np.array([3, 2, 1], dtype=int)
    for i in range(len(sample_ll)):
        result[i] = sample_ll[i].get_value()
    assert np.array_equal(result, expected)

def test_is_empty(empty_ll):
    assert empty_ll.is_empty()

def test_peek_first(sample_ll):
    assert 3 == sample_ll.peek_first()

def test_peek_last(sample_ll):
    assert 1 == sample_ll.peek_last()

def test_peek_first_empty(empty_ll):
    with pytest.raises(ListEmpty):
        empty_ll.peek_first()


if __name__ == "__main__":
    pytest.main()
