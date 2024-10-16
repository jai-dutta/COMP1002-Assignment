import time
from random import randint

from MinHeap import *
import numpy as np
from Vehicle import Vehicle

class VehicleEntry:
    def __init__(self, priority: float, vehicle: Vehicle):
        self.priority = priority
        self.vehicle = vehicle

    def __str__(self):
        return f"Priority: {self.priority} | Vehicle ID: {self.vehicle}"

    def get_priority(self):
        return self.priority

    def set_priority(self, priority):
        self.priority = priority

    def get_vehicle(self):
        return self.vehicle

    def set_vehicle(self, vehicle):
        self.vehicle = vehicle


class VehicleSortHeap(MinHeap):
    def __init__(self, size):
        super().__init__(size)

    def add(self, priority: int, value: object):
        if self.size == self.count:
            raise HeapFullException()

        new_entry = VehicleEntry(priority, value)
        self.heap[self.count] = new_entry
        self.trickle_up(self.count)
        self.count += 1

    def heapsort_vehicles(self, vehicles):
        # Clear the existing heap
        self.count = 0
        self.heap = np.empty(len(vehicles), dtype=object)

        # Add all vehicles to the heap
        for v in vehicles:
            self.add(v.get_distance_to_destination(), v)

        # Extract vehicles in sorted order (smallest to largest)
        sorted_vehicles = np.empty(len(vehicles), dtype=object)

        # Loop from the end of the array towards the start
        for i in range(len(vehicles)):
            sorted_vehicles[i] = self.remove().get_vehicle()

        return sorted_vehicles

    def find_nearest_vehicle(self, vehicles):
        if self.count == 0:
            raise HeapEmptyException("Heap empty")
        return self.heapsort_vehicles(vehicles)[0]


def quick_sort(arr):
    quick_sort_recurse(arr, 0, len(arr) - 1)
    return arr

def quick_sort_recurse(arr, left_index, right_index):
    if right_index > left_index:
        pivot_index = (left_index + right_index) // 2
        new_pivot_index = do_partitioning(arr, left_index, right_index, pivot_index)

        quick_sort_recurse(arr, left_index, new_pivot_index - 1)
        quick_sort_recurse(arr, new_pivot_index + 1, right_index)

def do_partitioning(arr, left_index, right_index, pivot_index):
    pivot_val = arr[pivot_index]
    arr[pivot_index], arr[right_index] = arr[right_index], arr[pivot_index]

    store_index = left_index
    for i in range(left_index, right_index):
        if arr[i].get_battery_level() > pivot_val.get_battery_level():
            if i != store_index:
                arr[i], arr[store_index] = arr[store_index], arr[i]
            store_index += 1

    arr[right_index], arr[store_index] = arr[store_index], arr[right_index]
    return store_index

def find_highest_battery_level(vehicles):
    quick_sort(vehicles)
    return vehicles[0]
