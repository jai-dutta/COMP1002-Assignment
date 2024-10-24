"""
Sorting.py

This file contains the sorting functions (heapsort and quicksort) for the simulation.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

import numpy as np

from MinHeap import *
from Vehicle import Vehicle


class VehicleEntry:
    """
    Class used to represent a vehicle entry in the heap.
    Attributes:
        priority: The priority of the vehicle. (In this case, the distance to destination)
        vehicle: The vehicle object.
    """
    def __init__(self, priority: float, vehicle: Vehicle):
        self.priority = priority
        self.vehicle = vehicle

    def __str__(self) -> str:
        return f"Priority: {self.priority} | Vehicle ID: {self.vehicle}"

    def get_priority(self) -> float:
        """
        Get the priority of the vehicle.
        """
        return self.priority

    def set_priority(self, priority: float):
        """
        Set the priority of the vehicle.
        """
        self.priority = priority

    def get_vehicle(self) -> Vehicle:
        """
        Return vehicle object
        """
        return self.vehicle

    def set_vehicle(self, vehicle: Vehicle):
        """
        Set the vehicle object.
        """
        self.vehicle = vehicle


class VehicleSortHeap(MinHeap):
    """
    Class used to represent a vehicle sort heap. Specialised MinHeap for storing vehicles and sorting them by distance to destination.
    Inherits from MinHeap.
    Changes:
        add: Adds a vehicle entry to the heap.
        heapsort_vehicles: Sorts the vehicles in the heap.
        find_nearest_vehicle: Finds the nearest vehicle to the destination.
    Attributes:
        size: The size of the heap. 
        heap: The heap array.
        count: The number of elements in the heap.
    """
    def __init__(self, size: int):
        super().__init__(size)

    def add(self, priority: float, value: Vehicle):
        """
        Add a vehicle entry to the heap.
        """
        if self.size == self.count:
            raise HeapFullException()

        new_entry = VehicleEntry(priority, value)
        self.heap[self.count] = new_entry
        self.trickle_up(self.count)
        self.count += 1

    def heapsort_vehicles(self, vehicles: np.ndarray) -> np.ndarray:
        """
        Sort the vehicles in the heap by distance to destination.
        """
        # Clear the existing heap
        self.count = 0
        self.heap = np.empty(len(vehicles), dtype=object)

        # Add all vehicles to the heap
        for v in vehicles:
            self.add(v.get_distance_to_destination(), v)

        # Loop from the end of the array towards the start
        for i in range(len(vehicles)):
            vehicles[i] = self.remove().get_vehicle()

        return vehicles

    def find_nearest_vehicle(self, vehicles: np.ndarray) -> Vehicle:
        """
        Find the nearest vehicle to it's destination using heapsort.
        """
        if self.count == 0:
            raise VehiclesEmptyException("No vehicles are in the AVMS.")
        return self.heapsort_vehicles(vehicles)[0]


def quick_sort(arr: np.ndarray) -> np.ndarray:
    """
    Main quicksort wrapper function.
    """
    quick_sort_recurse(arr, 0, len(arr) - 1)
    return arr


def quick_sort_recurse(arr: np.ndarray, left_index: int, right_index: int):
    """
    Recursive function to sort the vehicles by battery level using quicksort.
    """
    if right_index > left_index:
        pivot_index = (left_index + right_index) // 2
        new_pivot_index = do_partitioning(arr, left_index, right_index, pivot_index)

        quick_sort_recurse(arr, left_index, new_pivot_index - 1)
        quick_sort_recurse(arr, new_pivot_index + 1, right_index)


def do_partitioning(arr: np.ndarray, left_index: int, right_index: int, pivot_index: int) -> int:
    """
    Perform partitioning of the array.
    """
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


def find_highest_battery_level(vehicles: np.ndarray) -> Vehicle:
    """
    Find the vehicle with the highest battery level using quicksort.
    """
    quick_sort(vehicles)
    if len(vehicles) > 0:
        return vehicles[0]
    else:
        raise VehiclesEmptyException("No vehicles are in the AVMS.")
    
def find_nearest_vehicle(vehicles: np.ndarray) -> Vehicle:
    """
    Find the nearest vehicle to it's destination using heapsort.
    """
    heap = VehicleSortHeap(len(vehicles))
    return heap.find_nearest_vehicle(vehicles)

class VehiclesEmptyException(Exception):
    """
    Exception raised when there are no vehicles in the array.
    """
    pass

