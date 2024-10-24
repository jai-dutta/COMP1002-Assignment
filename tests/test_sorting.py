"""
test_sorting.py

This file contains the tests for the sorting algorithms.

DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
"""

import pytest

from Sorting import *
import numpy as np

@pytest.fixture
def sample_vehicles():
    vehicles = np.empty(3, dtype=Vehicle)

    vehicle1 = Vehicle("A", 10)
    vehicle1.set_distance_to_destination(100)

    vehicle2 = Vehicle("B", 20)
    vehicle2.set_distance_to_destination(50)

    vehicle3 = Vehicle("C", 30)
    vehicle3.set_distance_to_destination(10)

    vehicles[0] = vehicle1
    vehicles[1] = vehicle2
    vehicles[2] = vehicle3

    # vehicles will look like this:
    # Vehicle A battery_level=10, distance_to_destination=100,
    #  Vehicel B battery_level=20, distance_to_destination=50,
    #  Vehicle C battery_level=30, distance_to_destination=10
    return vehicles

@pytest.fixture
def heap():
    return VehicleSortHeap(5)

def test_quick_sort(sample_vehicles):
    quick_sort(sample_vehicles)
    assert sample_vehicles[0].get_distance_to_destination() == 10
    assert sample_vehicles[1].get_distance_to_destination() == 50
    assert sample_vehicles[2].get_distance_to_destination() == 100

def test_heap_sort(sample_vehicles, heap):
    heap.heapsort_vehicles(sample_vehicles)
    assert sample_vehicles[0].get_distance_to_destination() == 10
    assert sample_vehicles[1].get_distance_to_destination() == 50
    assert sample_vehicles[2].get_distance_to_destination() == 100

