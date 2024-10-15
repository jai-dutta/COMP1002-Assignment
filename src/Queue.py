from LinkedList import *

class Queue:
    """
        A class used to represent a queue. Linked list implementation.
    """
    def __init__(self):
        self.count = 0
        self.queue = LinkedList()

    def print_queue(self):
        self.queue.print_list()

    # return count of all elements in queue
    def get_count(self):
        return self.count
    
    # return true if queue is empty
    def is_empty(self):
        return self.count == 0
    
    # add value to end of queue
    def enqueue(self, value):
        self.queue.insert_last(value)
        self.count += 1

    # return and remove first value from queue
    def dequeue(self):
        if self.is_empty():
            raise IndexError("can't dequeue from empty queue!")
        self.count -= 1
        return self.queue.remove_first()
        
    # return first value of queue
    def peek(self):
        if self.is_empty():
            raise IndexError("can't peek into empty queue!")
        return self.queue.peek_first()
