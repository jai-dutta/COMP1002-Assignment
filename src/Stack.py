"""
Stack.py
DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
This file contains the Stack class.
"""

from LinkedList import LinkedList


class Stack:
    """
    A class used to represent a stack. Linked list implementation.

    """

    def __init__(self):
        self.stack = LinkedList()
        # count to keep track of items
        self.count = 0

    # return count of items in stack
    def get_count(self):
        return self.count

    # return true if stack is empty
    def is_empty(self):
        return self.count == 0

    # return top element
    def top(self):
        if self.is_empty():
            raise IndexError("no top of empty stack!")
        else:
            return self.stack.peek_first()

    # push value to top of stack
    def push(self, value):
        self.stack.insert_first(value)
        self.count += 1

    # return and delete top element
    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack!")
        else:
            self.count -= 1
            value = self.stack.peek_first()
            self.stack.remove_first()
            return value
