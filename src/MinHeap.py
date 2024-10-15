
# COMP1002 - Data Structures and Algorithms
# Practical 08 - Author: Jai Dutta
# Date: 8/10/2024  - SEMESTER 2 B-COMP
#
# This file contains the class for Heap and HeapEntry

import numpy as np
from Vehicle import Vehicle

class VehicleEntry:
    def __init__(self, priority: float, vehicle: Vehicle):
        self.priority = priority
        self.vehicle = vehicle

    def __str__(self):
        return f"Priority: {self.priority} | Vehicle ID: {self.vehicle.get_id()}"

    def get_priority(self):
        return self.priority

    def set_priority(self, priority):
        self.priority = priority

    def get_vehicle(self):
        return self.vehicle

    def set_vehicle(self, vehicle):
        self.vehicle = vehicle

class MinHeap:
    def __init__(self, size):
        self.size = size
        self.heap = np.empty(size, dtype=object)
        self.count = 0

    def add(self, priority: int, value: object):
        if self.size == self.count:
            raise HeapFullException()

        new_entry = VehicleEntry(priority, value)
        self.heap[self.count] = new_entry
        self.trickle_up(self.count)
        self.count += 1

    # iterative
    def trickle_up(self, current_index):
        parent_index = (current_index-1) // 2
        while current_index > 0 and self.heap[current_index].get_priority() < self.heap[parent_index].get_priority():
            self.heap[parent_index], self.heap[current_index] = self.heap[current_index], self.heap[parent_index]
            current_index = parent_index
            parent_index = (current_index - 1) // 2

    def remove(self):
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

    def trickle_down(self, current_index, num_items):
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
        for i in range(self.count):
            print(f"[{i}] {self.heap[i]}")

    def heapify(self, arr):
        # replace heap with imported array
        for i in arr:
            if i is not None:
                self.add(i.get_priority(), i.get_value())

    def heap_sort(self, array):
        self.heapify(array)
        for i in range(self.count-1, 0, -1):
            self.heap[0], self.heap[i] = self.heap[i], self.heap[0]
            self.trickle_down(0, i)

    def get_count(self):
        return self.count
    
    def heapsort_vehicles(self, vehicles):
        # Clear the existing heap
        self.count = 0
        self.heap = np.empty(len(vehicles), dtype=object)

        # Add all vehicles to the heap
        for vehicle in vehicles:
            self.add(vehicle.get_distance_to_destination(), vehicle)

        # Extract vehicles in sorted order
        sorted_vehicles = []
        while self.count > 0:
            entry = self.remove()
            sorted_vehicles.append(entry.get_vehicle())

        return sorted_vehicles

    def find_nearest_vehicle(self):
        if self.count == 0:
            raise HeapEmptyException("No vehicles in the heap")
        return self.heap[0].get_vehicle()

class HeapFullException(Exception):
    def __init__(self, message="Heap is full"):
        super().__init__(message)

class HeapEmptyException(Exception):
    def __init__(self, message="Heap is empty"):
        super().__init__(message)
