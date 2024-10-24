"""
QueThis file contains the Queue class.ue.py

This file contains the Queue class, representing a queue using a linked list.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372

"""

from LinkedList import *


class Queue:
    """
        A class used to represent a queue. Linked list implementation.
        Attributes:
            count: The number of elements in the queue.
            queue: The linked list representing the queue.
    """

    def __init__(self):
        self.count = 0
        self.queue = LinkedList()

    def print_queue(self):
        """
        Print the queue.
        """
        self.queue.print_list()

    # return count of all elements in queue
    def get_count(self) -> int:
        """
        Get the count of all elements in the queue.
        """
        return self.count

    # return true if queue is empty
    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        """
        return self.count == 0

    # add value to end of queue
    def enqueue(self, value: any) -> None:
        """
        Enqueues a value to the end of the queue.
        """
        self.queue.insert_last(value)
        self.count += 1

    # return and remove first value from queue
    def dequeue(self) -> any:
        """
        Dequeues the first value from the queue.
        """
        if self.is_empty():
            raise IndexError("can't dequeue from empty queue!")
        self.count -= 1
        return self.queue.remove_first()

    # return first value of queue
    def peek(self) -> any:
        """
        Returns (but does not dequeue) the first value of the queue.
        """
        if self.is_empty():
            raise IndexError("can't peek into empty queue!")
        return self.queue.peek_first()
