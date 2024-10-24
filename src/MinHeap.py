"""
MinHeap.py

This file contains the MinHeap class, representing a Min Heap used for a priority queue for dijkstra's algorithm.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

import numpy as np


class PriorityQueueEntry:
    """
    A class to represent a priority queue entry.
    Attributes:
        priority: The priority of the entry.
        value: The value of the entry.
    """
    def __init__(self, priority: int, value: object):
        self.priority = priority
        self.value = value

    def __str__(self) -> str:
        return f"Priority: {self.priority} | Value: {self.value}"

    def get_priority(self) -> int:
        return self.priority

    def set_priority(self, priority: int):
        self.priority = priority

    def get_value(self) -> object:
        return self.value

    def set_value(self, value: object):
        self.value = value


class MinHeap:
    """
    A class to represent a MinHeap used for priority queue for dijkstra's algorithm.
    Attributes:
        size: The size of the heap.
        heap: The heap.
        count: The number of elements in the heap.
    """
    def __init__(self, size: int):
        self.size = size
        self.heap = np.empty(size, dtype=object)
        self.count = 0

    def add(self, priority: int, value: object):
        """
        Add an entry to the heap.
        Args:
            priority: The priority of the entry.
            value: The value of the entry.
        """
        if self.size == self.count:
            raise HeapFullException()

        new_entry = PriorityQueueEntry(priority, value)
        self.heap[self.count] = new_entry
        self.trickle_up(self.count)
        self.count += 1

    # iterative
    def trickle_up(self, current_index: int) -> None:
        """
        Trickle up the heap.
        """
        parent_index = (current_index - 1) // 2
        while current_index > 0 and self.heap[current_index].get_priority() < self.heap[parent_index].get_priority():
            self.heap[parent_index], self.heap[current_index] = self.heap[current_index], self.heap[parent_index]
            current_index = parent_index
            parent_index = (current_index - 1) // 2

    def remove(self) -> PriorityQueueEntry:
        """
        Remove the root node from the heap.
        """
        if self.count == 0:
            raise HeapEmptyException()

        root_node = self.heap[0]
        self.count -= 1

        # in case removing root node
        if self.count > 0:
            # put the last element to root position
            self.heap[0] = self.heap[self.count]
            self.trickle_down(0, self.count)

        return root_node
    
    def peek(self) -> PriorityQueueEntry:
        """
        Peek at the root node of the heap.
        """
        return self.heap[0]

    def trickle_down(self, current_index: int, num_items: int):
        """
        Trickle down the heap.
        """
        left_child_index = current_index * 2 + 1
        right_child_index = left_child_index + 1

        if left_child_index < num_items:
            large_index = left_child_index

            if right_child_index < num_items:
                if self.heap[left_child_index].get_priority() > self.heap[right_child_index].get_priority():
                    large_index = right_child_index

            if self.heap[large_index].get_priority() < self.heap[current_index].get_priority():
                self.heap[large_index], self.heap[current_index] = self.heap[current_index], self.heap[large_index]
                self.trickle_down(large_index, num_items)

    def display(self):
        """
        Display the heap.
        """
        for i in range(self.count):
            print(f"[{i}] {self.heap[i]}")

    def get_count(self):
        """
        Get the number of elements in the heap.
        """
        return self.count
    


class HeapFullException(Exception):
    """
    An exception to handle when the heap is full.
    """
    def __init__(self, message="Heap is full"):
        super().__init__(message)


class HeapEmptyException(Exception):
    """
    An exception to handle when the heap is empty.
    """
    def __init__(self, message="Heap is empty"):
        super().__init__(message)
