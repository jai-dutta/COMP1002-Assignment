"""
test_queue.py

This file contains the tests for the Queue class.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

import pytest

from Queue import *

@pytest.fixture
def empty_queue():
    return Queue()

@pytest.fixture
def sample_queue():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    return q

def test_print_queue(sample_queue, capsys):
    sample_queue.print_queue()
    captured = capsys.readouterr()
    assert captured.out == "[1] 1 -> [2] 2 -> [3] 3\n"

def test_get_count(sample_queue):
    assert sample_queue.get_count() == 3

def test_is_empty(empty_queue, sample_queue):
    assert empty_queue.is_empty()
    assert not sample_queue.is_empty()

def test_enqueue(empty_queue):
    empty_queue.enqueue(1)
    assert empty_queue.get_count() == 1
    assert empty_queue.peek() == 1
    assert not empty_queue.is_empty()

def test_dequeue(sample_queue):
    assert sample_queue.dequeue() == 1
    assert sample_queue.get_count() == 2
    assert sample_queue.peek() == 2

def test_peek(sample_queue, empty_queue):
    assert sample_queue.peek() == 1
    with pytest.raises(IndexError):
        assert empty_queue.peek()



