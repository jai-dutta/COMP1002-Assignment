"""
LinkedList.py
DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
This file contains the LinkedList class, which is used to represent a linked list.
"""

class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value

    def get_next(self):
        return self.next
    
    def get_prev(self):
        return self.prev
    
    def set_next(self, next_node: "ListNode"):
        self.next = next_node

    def set_prev(self, prev_node: "ListNode"):
        self.prev = prev_node

class LinkedListIterator:
    def __init__(self, head):
        self.current = head
    def __iter__(self):
        return self

    def __next__(self):
        if not self.current:
            raise StopIteration
        else:
            node = self.current
            self.current = self.current.get_next()
            return node


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def __iter__(self):
        return LinkedListIterator(self.head)

    def __getitem__(self, item):
        if item < 0:
            raise IndexError("Index must be non-negative")

        current = self.head
        current_item = 0

        while current is not None:
            if current_item == item:
                return current
            else:
                current = current.get_next()
                current_item += 1

        raise IndexError("Index out of bounds!")

    def __len__(self):
        return self.count

    def print_list(self):
        counter = 1
        if self.is_empty():
            print("List is empty.")

        current_node = self.head

        while current_node is not None:
            print(f"[{counter}] {current_node.get_value()}", end="")
            counter += 1
            if current_node.get_next() is not None:
                print(" -> ", end="")
            current_node = current_node.get_next()
        print()

    def insert_first(self, value):
        new_node = ListNode(value)

        # if empty, then initialise this new node as the head.
        if self.is_empty(): 
            self.head = new_node
            self.tail = new_node
        # if not empty, put the current head as the next in line for the new node. this makes the new node the new head
        else:
            new_node.set_next(self.head)
            self.head.set_prev(new_node)
            self.head = new_node
        self.count += 1


    def insert_before(self, value, find_index):
        new_node = ListNode(value)
        if self.is_empty():
            print("List is empty.")
            self.insert_first(value)
            return

        else:
            cn = self.head
            search_index = 0
            while search_index != find_index:
                cn = cn.get_next()
                search_index += 1
            if search_index == find_index:
                if cn is self.head:
                    new_node.set_next(self.head)
                    self.head.set_prev(new_node)
                    self.head = new_node

                else:
                    prev_node = cn.get_prev()
                    new_node.set_next(cn)
                    new_node.set_prev(prev_node)

                    if prev_node is not None:
                        prev_node.set_next(new_node)
                    cn.set_prev(new_node)
            self.count += 1


    def insert_at(self, value, find_index):
        new_node = ListNode(value)
        inserted = False

        if self.is_empty():
            self.insert_first(value)
            return

        else:
            cn = self.head
            search_index = 0
            while search_index != find_index:
                cn = cn.get_next()
                search_index += 1
            if search_index == find_index:
                if cn.get_next():
                    new_node.set_next(cn.get_next())
                    if cn.get_next():
                        cn.get_next().set_prev(new_node)
                    new_node.set_prev(cn)
                    cn.set_next(new_node)
                    inserted = True
                    self.count += 1
                else:
                    self.insert_last(value)
                    inserted = True

        if not inserted:
            print("Failed to insert value.")



    def insert_last(self, value):
        new_node = ListNode(value)

        # if empty, then init the new node as the head
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.set_next(new_node)
            new_node.set_prev(self.tail)
            self.tail = new_node
        self.count += 1

            
    def is_empty(self):
        return self.head is None
    
    def peek_first(self):
        if self.is_empty():
            raise ListEmpty()
        return self.head.get_value()
    
    def peek_last(self):
        if self.is_empty():
            raise ListEmpty()
        return self.tail.get_value()

    def remove_first(self):
        if self.is_empty():
            raise ListEmpty()
        
        node_value = self.head.get_value()
        self.head = self.head.get_next()

        if self.head is not None:
            self.head.set_prev(None)
        else:
            self.tail = None
        self.count -= 1
        return node_value
    
    def remove_last(self):
        if self.is_empty():
            raise ListEmpty()
        # if removing last node, set head to none
        elif self.head.get_next() is None:
            node_value = self.head.get_value()
            self.head = None
            self.tail = None
        else:
            node_value = self.tail.get_value()
            self.tail = self.tail.get_prev()
            self.tail.set_next(None)
        self.count -= 1
        return node_value

    def remove_at(self, index):
        if self.is_empty():
            raise ListEmpty()
        if index < 0 or self.count-1 < index:
            raise IndexError("Index was out of bounds for LinkedList object!")

        if index == 0:
            self.remove_first()
        elif index == self.count - 1:
            self.remove_last()
        else:
            cn = self.head
            search_index = 0
            while search_index != index:
                cn = cn.get_next()
                search_index += 1

            if search_index == index:
                cn.get_prev().set_next(cn.get_next())
                cn.get_next().set_prev(cn.get_prev())
            else:
                print("Index not found.")
            self.count -= 1

class ListEmpty(Exception):
    def __init__(self):
        super().__init__("ERROR - Linked list is empty!")
