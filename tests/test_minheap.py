"""
test_minheap.py

This file contains the tests for the MinHeap class.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

import pytest

from MinHeap import *

@pytest.fixture
def empty_heap():
    return MinHeap(10)

@pytest.fixture
def sample_heap():
    mh = MinHeap(10)
    mh.add(50, "A")
    mh.add(10, "B")
    mh.add(1000, "C")
    return mh

def test_insert(empty_heap):
    empty_heap.add(1, "A")
    assert empty_heap.get_count() == 1
    assert empty_heap.peek().get_priority() == 1
    assert empty_heap.peek().get_value() == "A"

def test_remove(sample_heap):

    removed = sample_heap.remove()  
    assert removed.get_priority() == 10
    assert removed.get_value() == "B"
    assert sample_heap.get_count() == 2

    removed = sample_heap.remove()
    assert removed.get_priority() == 50
    assert removed.get_value() == "A"
    assert sample_heap.get_count() == 1

    removed = sample_heap.remove()
    assert removed.get_priority() == 1000
    assert removed.get_value() == "C"
    assert sample_heap.get_count() == 0

def test_display(sample_heap, capsys):
    sample_heap.display()
    captured = capsys.readouterr()
    assert captured.out == "[0] Priority: 10 | Value: B\n[1] Priority: 50 | Value: A\n[2] Priority: 1000 | Value: C\n"

if __name__ == "__main__":
    pytest.main()
