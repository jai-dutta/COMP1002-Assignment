"""
test_stack.py

This file contains the tests for the Stack class.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

import pytest

from Stack import *

@pytest.fixture
def empty_stack():
    return Stack()

@pytest.fixture
def sample_stack():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    return s

def test_get_count(sample_stack, empty_stack):
    assert sample_stack.get_count() == 3
    assert empty_stack.get_count() == 0

def test_is_empty(sample_stack, empty_stack):
    assert not sample_stack.is_empty()
    assert empty_stack.is_empty()

def test_top(sample_stack, empty_stack):
    assert sample_stack.top() == 3
    with pytest.raises(IndexError):
        empty_stack.top()

def test_push(empty_stack, sample_stack):
    empty_stack.push(1)
    assert empty_stack.get_count() == 1
    assert empty_stack.top() == 1

    sample_stack.push(4)
    assert sample_stack.get_count() == 4
    assert sample_stack.top() == 4

def test_pop(empty_stack, sample_stack):
    with pytest.raises(IndexError):
        empty_stack.pop()

    assert sample_stack.pop() == 3
    assert sample_stack.get_count() == 2
    assert sample_stack.top() == 2





