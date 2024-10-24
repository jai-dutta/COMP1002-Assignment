"""
LinkedList.py

This file contains the LinkedList class, which is used to represent a linked list.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""



class ListNode:
    """
    A class to represent a node in the linked list.
    Attributes:
        value: The value of the node.
        next: The next node in the linked list.
        prev: The previous node in the linked list.
    """

    def __init__(self, value: any):
        """
        Initialize a ListNode object.
        Args:
            value: The value of the node.
        """
        self.value = value
        self.next = None
        self.prev = None

    def get_value(self) -> any:
        """
        Return the value of the node.
        Returns:
            The value of the node.
        """
        return self.value

    def set_value(self, value: any):
        """
        Set the value of the node.
        Args:
            value: The value of the node.
        """
        self.value = value

    def get_next(self) -> "ListNode":
        """
        Return the next node in the linked list.
        Returns:
            The next node in the linked list.
        """
        return self.next

    def get_prev(self) -> "ListNode":
        """
        Return the previous node in the linked list.
        Returns:
            The previous node in the linked list.
        """
        return self.prev

    def set_next(self, next_node: "ListNode"):
        """
        Set the next node in the linked list.
        Args:
            next_node: The next node in the linked list.
        """
        self.next = next_node

    def set_prev(self, prev_node: "ListNode"):
        """
        Set the previous node in the linked list.
        Args:
            prev_node: The previous node in the linked list.
        """
        self.prev = prev_node


class LinkedListIterator:
    """
    An iterator for the linked list.
    Attributes:
        current: The current node in the linked list.
    """

    def __init__(self, head: ListNode):
        self.current = head

    def __iter__(self):
        return self

    def __next__(self) -> ListNode:
        if not self.current:
            raise StopIteration
        else:
            node = self.current
            self.current = self.current.get_next()
            return node


class LinkedList:
    """
    A class to represent a linked list.
    Attributes:
        head: The head node of the linked list.
        tail: The tail node of the linked list.
        count: The number of nodes in the linked list.
    """

    def __init__(self):
        """
        Initialize a LinkedList object.
        """
        self.head = None
        self.tail = None
        self.count = 0

    def __iter__(self):
        """
        Return an iterator for the linked list.
        Returns:
            An iterator for the linked list.
        """
        return LinkedListIterator(self.head)

    def __getitem__(self, item: int) -> ListNode:
        """
        Allows for index access in the linked list.
        Args:
            item: The index of the node to return.
        Returns:
            The node at the given index.
        """
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

    def __len__(self) -> int:
        """
        Return the number of nodes in the linked list.
        Returns:
            The number of nodes in the linked list.
        """
        return self.count

    def print_list(self):
        """
        Print the linked list.
        """
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

    def insert_first(self, value: any):
        """
        Insert a new node at the beginning of the linked list
        Args:
            value: The value of the new node.
        """
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

    def insert_before(self, value: any, find_index: int):
        """
        Insert a new node before the node at the given index.
        Args:
            value: The value of the new node.
            find_index: The index of the node to insert the new node before.
        """
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


    def insert_last(self, value: any):
        """
        Insert a new node at the end of the linked list.
        Args:
            value: The value of the new node.
        """
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

    def is_empty(self) -> bool:
        """
        Check if the linked list is empty.
        Returns:
            True if the linked list is empty, False otherwise.
        """
        return self.head is None

    def peek_first(self):
        """
        Return the value of the first node in the linked list.
        Returns:
            The value of the first node in the linked list.
        """
        if self.is_empty():
            raise ListEmpty()
        return self.head.get_value()

    def peek_last(self):
        """
        Return  the value of the last node in the linked list.
        Returns:
            The value of the last node in the linked list.
        """
        if self.is_empty():
            raise ListEmpty()
        return self.tail.get_value()

    def remove_first(self):
        """
        Remove the first node in the linked list.
        """
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
        """
        Remove the last node in the linked list.
        """
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
        """
        Remove the node at the given index.
        Args:
            index: The index of the node to remove.
        """
        if self.is_empty():
            raise ListEmpty()
        if index < 0 or self.count - 1 < index:
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
    """
    An exception to handle when the linked list is empty.
    """
    def __init__(self):
        super().__init__("ERROR - Linked list is empty!")
